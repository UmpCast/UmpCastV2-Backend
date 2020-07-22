from rest_framework.test import APITestCase
from backend import mixins
from model_bakery import baker
from ..models import League
from users.models import User
from django.urls import reverse
from rest_framework import status


class TestLeagueAPI(mixins.TestModelMixin, APITestCase):
    basename = 'league'
    filter_fields = ['user']
    valid_update = {
        'title': 'new league name',
        'description': 'new leagues require new descriptions!'
    }

    valid_create = {
        'title': 'foo league',
    }

    def create_object(self):
        return baker.make('leagues.League')

    def get_filter_queries(self):
        return {
            'user': [str(user.pk) for user in User.objects.all()]
        }
