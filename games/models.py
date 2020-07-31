from django.db import models
from ordered_model.models import OrderedModel

class Game(models.Model):
    division = models.ForeignKey('leagues.Division', on_delete=models.CASCADE)
    title = models.CharField(max_length=32)
    date_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    location = models.CharField(max_length=32)
    description = models.TextField(blank=True, max_length=1028, null=True)

    # ts
    ts_id = models.IntegerField(default=0)


class Post(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    role = models.ForeignKey('leagues.Role', on_delete=models.CASCADE)
    notes = models.TextField(blank=True, max_length=1028, null=True)


class Application(OrderedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    comments = models.TextField(blank=True, max_length=1028, null=True)
