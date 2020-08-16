from django.db import models
from django.utils.timezone import now
from django.contrib.postgres.fields import ArrayField


class TeamSnapNote(models.Model):
    notes = ArrayField(
        models.CharField(max_length=128), size=64
    )
    league = models.ForeignKey('leagues.League', on_delete=models.CASCADE)
    date_time = models.DateTimeField(default=now)

    class Meta:
        ordering = ['-date_time']

