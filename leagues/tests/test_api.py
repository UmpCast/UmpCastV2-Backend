from rest_framework.test import APITestCase
from backend import mixins
from model_bakery import baker
from ..models import League
from users.models import User
from django.urls import reverse
from rest_framework import status


class TestLeagueAPI(mixins.TestModelMixin, APITestCase):
    """
    League Model Tests for CRUD, List, List-Filter
    """

    basename = 'league'
    filter_fields = ['user']
    valid_update = {
        'title': 'new league name',
        'description': 'new leagues require new descriptions!'
    }

    valid_create = {
        'title': 'foo league',
    }

    def setUp(self):
        super().setUp()
        self.user.account_type = 'manager'

    def create_object(self):
        return baker.make('leagues.League')

    def get_filter_queries(self):
        return {
            'user': [str(user.pk) for user in User.objects.all()]
        }


class TestDivisionAPI(mixins.TestCreateMixin, mixins.TestDeleteMixin,
                        mixins.TestSetupMixin, APITestCase):
    """
    Division Model Tests for Create, Destroy
    """

    basename = 'division'

    def create_object(self):
        return baker.make('leagues.Division')

    def get_valid_create(self):
        league = baker.make('leagues.League')
        self.user.leagues.add(league, through_defaults = {'request_status': 'accepted'})
        return {
            'title': 'test division 1',
            'league': league.pk
        }

    def test_move(self):
        division_1 = baker.make('leagues.Division', order=0)
        division_2 = baker.make('leagues.Division', league=division_1.league, order=1)
        move_url = reverse('division-move', kwargs={'pk': division_1.pk})
        response = self.client.patch(move_url, data = {"order": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TestLevelAPI(mixins.TestCreateMixin, mixins.TestDeleteMixin,
                    mixins.TestFilterMixin, mixins.TestSetupMixin, APITestCase):
    """
    Level Model Tests for Create, Destroy, Filter, Move
    """

    basename = 'level'
    filter_fields = ['league']

    def create_object(self):
        return baker.make('leagues.Level')

    def get_valid_create(self):
        role = baker.make('leagues.Role')
        self.user.leagues.add(role.division.league, through_defaults = {'request_status': 'accepted'})
        return {
            'league': role.division.league.pk,
            'visibilities': [role.pk]
        }

    def get_filter_queries(self):
        return {
            'league': [str(league.pk) for league in League.objects.all()]
        }

    def test_move(self):
        level_1 = baker.make('leagues.Level', order=0)
        level_2 = baker.make('leagues.Level', league=level_1.league, order=1)
        move_url = reverse('level-move', kwargs={'pk': level_1.pk})
        response = self.client.patch(move_url, data = {"order": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestRoleAPI(mixins.TestCreateMixin, mixins.TestDeleteMixin,
                    mixins.TestSetupMixin, APITestCase):
    """
    Role Model Tests for Create, Destroy
    """

    basename = 'role'

    def create_object(self):
        return baker.make('leagues.Role')

    def get_valid_create(self):
        division = baker.make('leagues.Division')
        self.user.leagues.add(division.league, through_defaults = {'request_status': 'accepted'})
        return {
            'title': 'test role 1',
            'division': division.pk
        }

    def test_move(self):
        role_1 = baker.make('leagues.Role', order=0)
        role_2 = baker.make('leagues.Role', division=role_1.division, order=1)
        move_url = reverse('role-move', kwargs={'pk': role_1.pk})
        response = self.client.patch(move_url, data = {"order": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
