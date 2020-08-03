from rest_framework.test import APITestCase
from backend import mixins
from model_bakery import baker
from leagues.models import League, Division
from django.shortcuts import reverse
from rest_framework import status
from django.utils import timezone

class TestApplicationAPI(mixins.TestCreateMixin, mixins.TestDeleteMixin,
                            mixins.TestSetupMixin, APITestCase):
    """
    Test Application Models for Create, Destroy, Move
    """

    basename = 'application'

    def create_object(self):
        return baker.make('games.Application')

    def get_valid_create(self):
        post = baker.make('games.Post')
        self.user.leagues.add(post.game.division.league, through_defaults = {'request_status': 'accepted'})
        return {
            'post': post.pk,
            'user': self.user.pk
        }

    def test_move(self):
        app_1 = baker.make('games.Application', order=0)
        app_2 = baker.make('games.Application', post=app_1.post, order=1)
        move_url = reverse('application-move', kwargs={'pk': app_1.pk})
        response = self.client.patch(move_url, data = {"order": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPostAPI(mixins.TestCreateMixin, mixins.TestDeleteMixin,
                    mixins.TestSetupMixin, APITestCase):
    """
    Test Post Models for Create, Destroy
    """

    basename = 'post'

    def create_object(self):
        return baker.make('games.Post')

    def get_valid_create(self):
        game = baker.make('games.Game')
        role = baker.make('leagues.Role')
        self.user.leagues.add(game.division.league, through_defaults = {'request_status': 'accepted'})
        return {
            'game': game.pk,
            'role': role.pk
        }


class TestGameAPI(mixins.TestCreateMixin, mixins.TestRetrieveMixin,
                    mixins.TestDeleteMixin, mixins.TestListMixin, mixins.TestFilterMixin,
                    mixins.TestSetupMixin, APITestCase):
    """
    Test Game Models for Create, Retrieve, Destroy, List, List-Filter
    """

    basename = 'game'
    filter_fields = ['division', 'league']

    def create_object(self):
        return baker.make('games.Game')

    def get_valid_create(self):
        division = baker.make('leagues.Division')
        self.user.leagues.add(division.league, through_defaults = {'request_status': 'accepted'})
        return {
            'title': 'test_game_title',
            'date_time': timezone.now(),
            'location': 'test_location_name',
            'division': division.pk,
        }

    def get_filter_queries(self):
        baker.make('games.Game', _quantity=30)
        return {
            'division': [str(division.pk) for division in Division.objects.all()],
            'league': [str(league.pk) for league in League.objects.all()]
        }