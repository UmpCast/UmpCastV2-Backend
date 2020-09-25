from django.shortcuts import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from backend import mixins
from users.models import User


class TestUmpCastNotificationAPI(mixins.TestRetrieveMixin, mixins.TestListMixin,
                                 mixins.TestFilterMixin, mixins.TestSetupMixin, APITestCase):
    basename = 'ump-cast-notification'
    filter_fields = ['date_time_before', 'date_time_after']

    def create_object(self):
        return baker.make('notifications.UmpCastNotification')

    def get_filter_queries(self):
        return {
            'date_time_before': ['2020-07-31T02:29:28.982442Z'],
            'date_time_after': ['2020-07-31T02:29:28.982442Z']
        }


class TestLeagueNotificationAPI(mixins.TestModelMixin, APITestCase):
    basename = 'league-notification'
    filter_fields = ['date_time_before', 'date_time_after', 'user']
    valid_update = {
        'message': 'A new message has been created'
    }

    def create_object(self):
        return baker.make('notifications.LeagueNotification')

    def get_filter_queries(self):
        return {
            'user': [str(user.pk) for user in User.objects.all()],
            'date_time_before': ['2020-07-31T02:29:28.982442Z'],
            'date_time_after': ['2020-07-31T02:29:28.982442Z']
        }

    def get_valid_create(self):
        league = baker.make('leagues.League')
        self.user.leagues.add(league, through_defaults={
                              'request_status': 'accepted'})
        return {
            'subject': 'Message Subject',
            'message': 'Message Body',
            'league': league.pk
        }


class TestGameNotificationAPI(mixins.TestRetrieveMixin, mixins.TestListMixin,
                              mixins.TestFilterMixin, mixins.TestSetupMixin, APITestCase):
    basename = 'game-notification'
    filter_fields = ['date_time_before', 'date_time_after', 'user']

    def create_object(self):
        return baker.make('notifications.GameNotification')

    def get_filter_queries(self):
        return {
            'user': [str(user.pk) for user in User.objects.all()],
            'date_time_before': ['2020-07-31T02:29:28.982442Z'],
            'date_time_after': ['2020-07-31T02:29:28.982442Z']
        }


class TestApplicationNotificationAPI(mixins.TestRetrieveMixin, mixins.TestListMixin,
                                     mixins.TestFilterMixin, mixins.TestSetupMixin, APITestCase):
    basename = 'application-notification'
    filter_fields = ['date_time_before', 'date_time_after', 'user']

    def create_object(self):
        return baker.make('notifications.ApplicationNotification')

    def get_filter_queries(self):
        return {
            'user': [str(user.pk) for user in User.objects.all()],
            'date_time_before': ['2020-07-31T02:29:28.982442Z'],
            'date_time_after': ['2020-07-31T02:29:28.982442Z']
        }


class TestNotificationListAPI(mixins.TestSetupMixin, APITestCase):

    def test_notification_list_endpoint(self):
        league = baker.make('leagues.League')
        baker.make('notifications.UmpCastNotification', _quantity=10)
        baker.make('notifications.LeagueNotification', _quantity=10)
        game = baker.make('games.Game', division__league=league)
        app = baker.make('games.Application', post__game=game, user=self.user)
        baker.make('notifications.GameNotification', game=game, _quantity=10)
        baker.make('notifications.ApplicationNotification',
                   application=app, _quantity=10)
        list_url = reverse('notification-list', kwargs={'pk': self.user.pk})
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
