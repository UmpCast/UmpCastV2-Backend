from rest_framework.test import APITestCase
from backend import mixins
from leagues.models import League
from django.shortcuts import reverse
from model_bakery import baker
from rest_framework import status


class TestTeamSnapAPI(mixins.TestListMixin, mixins.TestFilterMixin,
                      mixins.TestSetupMixin, APITestCase):
    basename = 'teamsnap-note'
    filter_fields = ['league']

    def get_filter_queries(self):
        return {
            'league': [str(league.pk) for league in League.objects.all()]
        }


class TestTeamSnapBuildAPI(mixins.TestSetupMixin, APITestCase):
    """
    Doesn't actually send TeamSnap requests. Only check endpoint availability
    """

    def test_get_build(self):
        league = baker.make('leagues.League')
        url = f"{reverse('teamsnap-build', kwargs={'pk': league.pk})}?api_key={league.api_key}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_build(self):
        league = baker.make('leagues.League')
        url = f"{reverse('teamsnap-build', kwargs={'pk': league.pk})}?api_key={league.api_key}"
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestTeamSnapSyncAPI(mixins.TestSetupMixin, APITestCase):
    """
    Doesn't actually send TeamSnap requests. Only check endpoint availability
    """

    def test_get_sync(self):
        league = baker.make('leagues.League')
        url = f"{reverse('teamsnap-sync', kwargs={'pk': league.pk})}?api_key={league.api_key}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
