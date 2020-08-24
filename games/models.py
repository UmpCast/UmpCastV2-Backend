from django.db import models
from django.db.models.signals import post_save
from ordered_model.models import OrderedModel

from backend.mixins import OrderedModelUpdateMixin


class Game(models.Model):
    division = models.ForeignKey('leagues.Division', on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    date_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    location = models.CharField(max_length=128)
    description = models.TextField(blank=True, max_length=1028, null=True)

    # ts
    ts_id = models.IntegerField(default=0)

    class Meta:
        ordering = ['date_time']

    def sync(self, **kwargs):
        # expected fields: division, title, date_time, location, is_active
        attrs = ['title', 'date_time', 'location', 'is_active']
        update_fields = []
        exception_notes = []

        if self.division != kwargs['division']:
            ts_id = self.ts_id
            exception_notes.append(
                f"{self.title} changed divisions on teamsnap. The original game has been deleted"
            )
            self.delete()
            game = Game.objects.create(
                division=kwargs['division'], title=kwargs['title'],
                date_time=kwargs['date_time'], is_active=kwargs['is_active'],
                location=kwargs['location'], ts_id=ts_id
            )
            exception_notes.append(
                f"{self.title} has been created"
            )
            return exception_notes

        for attr in attrs:
            if getattr(self, attr) != kwargs[attr]:
                update_fields.append(attr)
                self.attr = kwargs[attr]
        if update_fields:
            self.save(update_fields=update_fields)
            exception_notes.append(
                f"{self.title} had the following items updated: {', '.join(update_fields)}"
            )
        return exception_notes


class Post(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    role = models.ForeignKey('leagues.Role', on_delete=models.CASCADE)
    notes = models.TextField(blank=True, max_length=1028, null=True)


def create_posts_from_game(sender, instance, *args, **kwargs):
    if kwargs['created']:
        for role in instance.division.role_set.all():
            Post.objects.create(game=instance, role=role)


post_save.connect(create_posts_from_game, sender=Game)


class Application(OrderedModelUpdateMixin, OrderedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    comments = models.TextField(blank=True, max_length=1028, null=True)
    order_with_respect_to = 'post'
