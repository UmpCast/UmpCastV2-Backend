from django.db import models
from django.utils.timezone import now
from datetime import datetime
from django.contrib.postgres.fields import JSONField


class League(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=1028, null=True, blank=True)
    league_picture = models.ImageField(upload_to='league_pics/%Y/%m/', null=True, blank=True)
    date_joined = models.DateTimeField(default=now)
    expiration_date = models.DateTimeField(default=now+datetime.timedelta(days=14))
    adv_scheduling_limit = models.IntegerField(default=30)  # how many days in advance games are scheduled

    # team snap fields
    ts_id = models.IntegerField(default=0)
    api_key = models.CharField(default="", max_length=128)
    opponent_library = JSONField(default=dict, blank=True)

    def __str__(self):
        return self.title


class ApplyLeagueCode(models.Model):
    code = models.CharField(max_length=16, unique=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    expiration_date = models.DateTimeField(default=now+datetime.timedelta(days=7))

    def __str__(self):
        return self.code


class Division(models.Model):
    title = models.CharField(max_length=64)
    league = models.ForeignKey(League, on_delete=models.CASCADE)

    # team snap fields
    ts_id = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Role(models.Model):
    title = models.CharField(max_length=64)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)

    def __str__(self):
        return ' '.join([self.division.title, self.title])






