import requests
import json
import jmespath
from games.models import Game
from leagues.models import League, Division
from datetime import datetime


class JMESPathQueryBuilder(object):

    @staticmethod
    def get_data_query(queries):
        """
        jmespath query helper method: creates a query string based on a list of
        queries. adds each query result into a dictionary structure
        """
        return ','.join([f"{query}: data[?name=='{query}'] | [0].value" for query in queries ])


    @staticmethod
    def get_links_query(queries):
        """
        jmespath query helper method: creates a query string based on a list of
        queries. adds each query result into a dictionary structure
        """
        return ','.join([f"{query}_link: links[?rel=='{query}'] | [0].href" for query in queries])


class TeamSnapBaseMixin(object):
    entry_url = 'https://api.teamsnap.com/v3/me'

    def get_tree_url(self):
        """
        Starting from the entry_url, returns the url which displays the division tree
        structure for a given league
        """

        assert hasattr(self, "header"), (
            "'%s' must define the header attribute when inheriting from TeamSnapBaseMixin, "
            % self.__class__.__name__
        )

        user_json = json.loads(requests.get(self.entry_url, headers=self.header).text)
        root_division_query = "collection.items[0].links[?rel=='divisions'] | [0].href"
        root_division_path = jmespath.search(root_division_query, user_json)

        root_division_json = json.loads(requests.get(root_division_path, headers=self.header).text)
        tree_search_query = "collection.items[0].links[?rel=='tree'] | [0].href"
        return jmespath.search(tree_search_query, root_division_json)


    def get_tree_components(self):
        """
        Starting with the tree url, parse the json response and create a consistent
        data structure with each division.
        Each division dictionary contains: id, name, parent_id, division_events_link
        """
        tree_url = self.get_tree_url()
        tree_json = json.loads(requests.get(tree_url, headers=self.header).text)

        data_query = JMESPathQueryBuilder.get_data_query(['id', 'name', 'parent_id'])
        links_query = JMESPathQueryBuilder.get_links_query(['division_events'])
        query_string = f"collection.items[*].{{ {data_query}, {links_query} }}"
        return jmespath.search(query_string, tree_json)


    @staticmethod
    def get_id_name_mappings(tree_components):
        mappings = {}
        for component in tree_components:
            mappings[component['id']] = component['name']
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

        for component in tree_components:
            parent_id = component['parent_id']
            curr_id = component['id']
            if parent_id is None:
                adjacency_dict['root'] = curr_id
            elif parent_id in adjacency_dict:
                adjacency_dict[parent_id].append(curr_id)
            else:
                adjacency_dict[parent_id] = [curr_id]

        adjacency_dict['mappings'] = self.get_id_name_mappings(tree_components)
        return adjacency_dict


    def create_league(self, divisions):
        """
        Clears out all the divisions within the current league and attatch
        new divisions as specified by divisions
        """
        self.league.division_set.all().delete()  # clear out divisions
        mappings = self.get_id_name_mappings(self.get_tree_components())
        for division in divisions:
            if division in mappings:  # check if division is even valid
                Division.objects.create(
                    title = mappings[division],
                    league = self.league,
                    ts_id = division
                )
            else:
                self.exception_notes.append(
                    f"Division with ts_id {division} was not created since it does not exist"
                )
