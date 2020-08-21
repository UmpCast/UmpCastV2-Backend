from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from backend import mixins
from leagues.models import League

from ..models import User


class TestUserAPI(mixins.TestCreateMixin, mixins.TestRetrieveMixin, mixins.TestUpdateMixin,
                  mixins.TestListMixin, mixins.TestFilterMixin, mixins.TestSetupMixin,
                  APITestCase):
    """
    User Model tests for CRUD, List, List-Filter, and Email Validation
    """

    basename = 'user'
    filter_fields = ['leagues', 'account_type']
    valid_create = {
        'email': 'valid@email.com',
        'first_name': 'validfirstname',
        'last_name': 'validlastname',
        'password': 'avalidpassword',
        'password2': 'avalidpassword'
    }
    valid_update = {
        'email': 'replacement@email.com'
    }

    def get_object(self):
        return self.user

    def get_filter_queries(self):
        league = baker.make('leagues.League')
        self.user.leagues.add(league)
        return {
            'leagues': [str(league.pk)],
            'account_type': ['inactive', 'umpire', 'manager']
        }

    def test_user_validate_unique(self):
        user = baker.make('users.User', email='duplicate@email.com')
        data = {
            'email': 'duplicate@email.com'
        }

        create_url = reverse('user-list')
        response = self.client.post(create_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'][0].code, 'unique')

    def test_user_validate_email(self):
        data = {
            'email': 'bad_email'
        }

        create_url = reverse('user-list')
        response = self.client.post(create_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'][0].code, 'invalid')

    def test_get_object_me_endpoint(self):
        retrieve_url = reverse('user-detail', kwargs={'pk': 'me'})
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestUserLeagueStatusAPI(mixins.TestModelMixin, APITestCase):
    """
    UserLeagueStatus ModelTestCases
    """

    basename = 'user-league-status'
    filter_fields = ['user', 'league', 'request_status', 'account_type']
    valid_update = {
        'max_casts': 101
    }

    def create_object(self):
        return baker.make('users.UserLeagueStatus')

    def get_filter_queries(self):
        return {
            'user': [str(user.pk) for user in User.objects.all()],
            'league': [str(league.pk) for league in League.objects.all()],
            'request_status': ['accepted', 'pending', 'rejected'],
            'account_type': ['manager', 'umpire']
        }

    def get_valid_create(self):
        return {
            'user': self.user.pk,
            'league': baker.make('leagues.League').pk,
        }

    def test_apply_level(self):
        uls = baker.make('users.UserLeagueStatus', user=self.user)
        level = baker.make('leagues.Level', league=uls.league)
        self.user.leagues.add(level.league, through_defaults={
                              'request_status': 'accepted'})
        url = reverse('user-league-status-apply-level', kwargs={'pk': uls.pk})
        response = self.client.post(url, data={"level": level.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
