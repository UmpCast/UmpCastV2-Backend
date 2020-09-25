import json
from datetime import datetime

import jmespath
import requests

from games.models import Game
from leagues.models import Division, League


class JMESPathQueryBuilder(object):

    @staticmethod
    def get_data_query(queries):
        """
        jmespath query helper method: creates a query string based on a list of
        queries. adds each query result into a dictionary structure
        """
        return ','.join([f"{query}: data[?name=='{query}'] | [0].value" for query in queries])

    @staticmethod
    def get_links_query(queries):
        """
        jmespath query helper method: creates a query string based on a list of
        queries. adds each query result into a dictionary structure
        """
        return ','.join([f"{query}_link: links[?rel=='{query}'] | [0].href" for query in queries])


class TeamSnapBaseMixin(object):
    entry_url = 'https://api.teamsnap.com/v3/me'

    def valid_key(self):
        assert hasattr(self, "header"), (
            "'%s' must define the header attribute when inheriting from TeamSnapBaseMixin, "
            % self.__class__.__name__
        )
        user_json = json.loads(requests.get(
            self.entry_url, headers=self.header).text)
        return not 'error' in user_json['collection']

    def get_tree_url(self):
        """
        Starting from the entry_url, returns the url which displays the division tree
        structure for a given league
        """

        assert hasattr(self, "header"), (
            "'%s' must define the header attribute when inheriting from TeamSnapBaseMixin, "
            % self.__class__.__name__
        )

        user_json = json.loads(requests.get(
            self.entry_url, headers=self.header).text)
        root_division_query = "collection.items[0].links[?rel=='divisions'] | [0].href"
        root_division_path = jmespath.search(root_division_query, user_json)

        root_division_json = json.loads(requests.get(
            root_division_path, headers=self.header).text)
        tree_search_query = "collection.items[0].links[?rel=='tree'] | [0].href"
        return jmespath.search(tree_search_query, root_division_json)

    def get_tree_components(self):
        """
        Starting with the tree url, parse the json response and create a consistent
        data structure with each division.
        Each division dictionary contains: id, name, parent_id, division_events_link
        """
        tree_url = self.get_tree_url()
        tree_json = json.loads(requests.get(
            tree_url, headers=self.header).text)

        data_query = JMESPathQueryBuilder.get_data_query(
            ['id', 'name', 'parent_id'])
        links_query = JMESPathQueryBuilder.get_links_query(['division_events'])
        query_string = f"collection.items[*].{{ {data_query}, {links_query} }}"
        return jmespath.search(query_string, tree_json)

    @staticmethod
    def get_id_value_mappings(tree_components, value):
        mappings = {}
        for component in tree_components:
            mappings[component['id']] = component[value]
        return mappings


class TeamSnapBuilder(TeamSnapBaseMixin):

    def __init__(self, token, league):
        self.header = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {token}"
        }
        self.league = league
        self.exception_notes = []

    def build_tree(self):
        """
        Using a list of tree_components, create the underlying tree structure
        Returns a dictionary with: root, parent_id: [children_ids], mappings
        """
        tree_components = self.get_tree_components()
        adjacency_dict = {}
        response = {}

        for component in tree_components:
            parent_id = component['parent_id']
            curr_id = str(component['id'])
            if parent_id is None:
                response['root'] = curr_id
            elif parent_id in adjacency_dict:
                adjacency_dict[parent_id].append(curr_id)
            else:
                adjacency_dict[parent_id] = [curr_id]

        response['tree'] = adjacency_dict
        response['mappings'] = self.get_id_value_mappings(
            tree_components, 'name')
        return response

    def create_league(self, divisions):
        """
        Clears out all the divisions within the current league and attatch
        new divisions as specified by divisions
        """
        for division in self.league.division_set.all():  # clear out divisions
            self.exception_notes.append(
                f"{division.title} and all related games removed from UmpCast"
            )
            division.delete()
        mappings = self.get_id_value_mappings(
            self.get_tree_components(), 'name')
        for division in divisions:
            if division in mappings:  # check if division is even valid
                try:
                    d = Division.objects.create(
                        title=mappings[division][:32],
                        league=self.league,
                        ts_id=division
                    )
                    self.exception_notes.append(
                        f"{d.title} was succesfully created by UmpCast"
                    )
                except:
                    self.exception_notes.append(
                        f"An unexpected error occured while creating {division}. Division not created"
                    )
            else:
                self.exception_notes.append(
                    f"UmpCast could not find {division}"
                )


class TeamSnapSyncer(TeamSnapBaseMixin):

    def __init__(self, token, league):
        self.header = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {token}"
        }
        self.league = league
        self.exception_notes = []
        self.memory = {
            'team': {},
            'opponent': {},
            'division_location': {},
            'location': {}
        }

    def get_teamsnap_attribute(self, attr, attr_id, attr_link):
        """
        Return the value of the attribute from memory or send a request and update memory
        """
        if attr_id in self.memory[attr]:
            return self.memory[attr][attr_id]
        teamsnap_json = json.loads(requests.get(
            attr_link, headers=self.header).text)
        query = "collection.items[0].data[?name=='name'] | [0].value"
        name = jmespath.search(query, teamsnap_json)
        self.memory[attr][attr_id] = name
        return name

    def get_game_title(self, team_id, team_link, opponent_id, opponent_link):
        """
        Gets the UmpCast generated title for a given division_event based on
        team_id and opponent_id
        """
        try:
            team_name = self.get_teamsnap_attribute('team', team_id, team_link)
        except:
            team_name = 'Name Not Found'
        try:
            opponent_name = self.get_teamsnap_attribute(
                'opponent', opponent_id, opponent_link)
        except:
            opponent_name = 'Name Not Found'
        return f"{team_name} vs. {opponent_name}"

    def get_location_title(self, division_location_id, division_location_link, location_id, location_link):
        try:
            if division_location_id:
                return self.get_teamsnap_attribute('division_location', division_location_id, division_location_link)
            if location_id:
                return self.get_teamsnap_attribute('location', location_id, location_link)
            return "Location Not Found"
        except:
            return "Location Not Found"

    @staticmethod
    def parse_utc_string(utc_string):
        """
        Convert from iso-z format to pure iso format. Returns utc timezone aware datetime
        """
        return datetime.fromisoformat(utc_string.replace('Z', '+00:00'))

    def sync_game(self, info, division):
        title = self.get_game_title(
            info['team_id'], info['team_link'], info['opponent_id'], info['opponent_link'])[:128]  # enforce character limit
        try:
            date_time = self.parse_utc_string(info['start_date'])
        except:
            self.exception_notes.append(
                f"{title} was not synced since UmpCast could not find the start time"
            )
            return
        location = self.get_location_title(
            info['division_location_id'], info['division_location_link'], info['location_id'], info['location_link'])[:128]  # enforce character limit
        if Game.objects.filter(ts_id=info['id']).exists():
            game = Game.objects.get(ts_id=info['id'])
            self.exception_notes += game.sync(title=title, date_time=date_time,
                                              location=location, division=division, is_active=info['is_canceled'])
        else:
            game = Game.objects.create(
                division=division, title=title,
                date_time=date_time, is_active=info['is_canceled'],
                location=location, ts_id=info['id']
            )
            self.exception_notes.append(
                f"{game.title} was discovered by UmpCast"
            )

    def sync_division(self, url, division):
        """
        Given a given division url, create a list of division_events info objects in that division
        and call the method to sync those division_events
        """
        events_json = json.loads(requests.get(url, headers=self.header).text)
        data_query = JMESPathQueryBuilder.get_data_query([
            "id", "is_canceled", "division_location_id", "location_id", "start_date",
            "team_id", "opponent_id", "is_game", "division_id"
        ])

        links_query = JMESPathQueryBuilder.get_links_query([
            "division_location", "location", "opponent", "team"
        ])
        query = f"collection.items[*].{{ {data_query} , {links_query} }}"
        events = jmespath.search(query, events_json)
        for event in events:
            try:
                self.sync_game(event, division)
            except Exception as e:
                self.exception_notes.append(
                    f"An unexpected error occured while syncing {event['id']}. Other games unaffected"
                )
                self.exception_notes.append(e)

    def sync(self):
        tree_components = self.get_tree_components()
        mappings = self.get_id_value_mappings(
            tree_components, 'division_events_link')
        for division in self.league.division_set.all():
            if division.ts_id != 0 and division.ts_id in mappings:
                try:
                    self.sync_division(mappings[division.ts_id], division)
                except:
                    self.exception_notes.append(
                        f"An unexpected error occured while syncing {division.title}. Certain games in the division may not have been synced"
                    )
            else:
                self.exception_notes.append(
                    f"{division.title} was not synced by UmpCast."
                )
