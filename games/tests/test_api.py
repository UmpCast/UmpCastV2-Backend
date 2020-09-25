from datetime import timedelta

from django.shortcuts import reverse
from django.utils import timezone
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from backend import mixins
from leagues.models import Division, League
from users.models import UserLeagueStatus


class TestApplicationAPI(mixins.TestCreateMixin, mixins.TestDeleteMixin, mixins.TestListMixin,
                         mixins.TestFilterMixin, mixins.TestSetupMixin, APITestCase):
    """
    Test Application Models for Create, Destroy, Move
    """

    basename = 'application'
    filter_fields = ['user', 'date_time_before', 'date_time_after']

    def create_object(self):
        return baker.make('games.Application', post__game__date_time=timezone.now()+timedelta(days=10))

    def get_valid_create(self):
        league = baker.make('leagues.League')
        post = baker.make('games.Post', game__date_time=timezone.now()+timedelta(days=10), game__division__league=league,
                          role__division__league=league)
        self.user.leagues.add(league, through_defaults={
                              'request_status': 'accepted'})
        uls = UserLeagueStatus.objects.get(user=self.user, league=league)
        uls.visibilities.add(post.role)
        return {
            'post': post.pk,
            'user': self.user.pk
        }

    def get_filter_queries(self):
        applications = baker.make(
            'games.Application', user=self.user, _quantity=10)
        return {
            'user': [str(self.user.pk)],
            'date_time_before': ['2020-07-31T02:29:28.982442Z'],
            'date_time_after': ['2020-07-31T02:29:28.982442Z']
        }

    def test_cast_endpoint(self):
        application = baker.make('games.Application')
        cast_url = reverse('application-cast', kwargs={'pk': application.pk})
        response = self.client.patch(cast_url)
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
        self.user.leagues.add(game.division.league, through_defaults={
                              'request_status': 'accepted'})
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
    filter_fields = ['division', 'date_time_before',
                     'date_time_after', 'division__in']

    def create_object(self):
        return baker.make('games.Game')

    def get_valid_create(self):
        division = baker.make('leagues.Division')
        self.user.leagues.add(division.league, through_defaults={
                              'request_status': 'accepted'})
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
            'date_time_before': ['2020-07-31T02:29:28.982442Z'],
            'date_time_after': ['2020-07-31T02:29:28.982442Z'],
            'division__in': [', '.join([str(division.pk) for division in Division.objects.all()])]
        }
