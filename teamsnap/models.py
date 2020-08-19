from django.db import models
from django.utils.timezone import now


class TeamSnapNote(models.Model):
    league = models.ForeignKey('leagues.League', on_delete=models.CASCADE)
    date_time = models.DateTimeField(default=now)

    class Meta:
        ordering = ['-date_time']


class TeamSnapNoteItem(models.Model):
    teamsnap_note = models.ForeignKey(TeamSnapNote, on_delete=models.CASCADE)
    note = models.CharField(max_length=128)
