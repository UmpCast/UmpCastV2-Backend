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
        self.user.leagues.add(league)
        return {
            'title': 'test division 1',
            'league': league.pk
        }


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
        self.user.leagues.add(division.league)
        return {
            'title': 'test role 1',
            'division': division.pk
        }
