from django.db import models
from ordered_model.models import OrderedModel
from django.db.models.signals import post_save

class Game(models.Model):
    division = models.ForeignKey('leagues.Division', on_delete=models.CASCADE)
    title = models.CharField(max_length=32)
    date_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    location = models.CharField(max_length=32)
    description = models.TextField(blank=True, max_length=1028, null=True)

    # ts
    ts_id = models.IntegerField(default=0)

    class Meta:
        ordering = ['-date_time']


class Post(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    role = models.ForeignKey('leagues.Role', on_delete=models.CASCADE)
    notes = models.TextField(blank=True, max_length=1028, null=True)


def create_posts_from_game(sender, instance, *args, **kwargs):
    if kwargs['created']:
        for role in instance.division.role_set.all():
            Post.objects.create(game=instance, role=role)

post_save.connect(create_posts_from_game, sender=Game)


class Application(OrderedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    comments = models.TextField(blank=True, max_length=1028, null=True)
