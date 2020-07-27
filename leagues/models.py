from django.db import models
from django.utils.timezone import now
from datetime import datetime, timedelta
from django.contrib.postgres.fields import JSONField
from ordered_model.models import OrderedModel


def set_league_expiration_date():
    return now() + timedelta(days=14)


def set_apply_league_expiration_date():
    return now() + timedelta(days=7)


class League(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=1028, null=True, blank=True)
    league_picture = models.ImageField(upload_to='league_pics/%Y/%m/', null=True, blank=True)
    date_joined = models.DateTimeField(default=now)
    expiration_date = models.DateTimeField(default=set_league_expiration_date)
    adv_scheduling_limit = models.IntegerField(default=30)  # how many days in advance games are scheduled
    public_access = models.BooleanField(default=False)
    can_apply = models.BooleanField(default=True)
    email = models.EmailField(max_length=64, blank=True,  null=True)
    website_url = models.CharField(max_length=64, blank=True, null=True)

    # team snap fields
    ts_id = models.IntegerField(default=0)
    api_key = models.CharField(default="", max_length=128)
    opponent_library = JSONField(default=dict, blank=True)

    def __str__(self):
        return self.title


class Division(models.Model):
    title = models.CharField(max_length=32)
    league = models.ForeignKey(League, on_delete=models.CASCADE)

    # team snap fields
    ts_id = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Role(models.Model):
    title = models.CharField(max_length=32)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)

    def __str__(self):
        return ' '.join([self.division.title, self.title])


class Level(OrderedModel):
    title = models.CharField(max_length=32, null=True, blank=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    roles = models.ManyToManyField(Role)
    order_with_respect_to = 'league'
