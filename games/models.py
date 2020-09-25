from django.db import models
from django.db.models.signals import post_save
from ordered_model.models import OrderedModel
from django.utils import timezone
from users.models import UserLeagueStatus

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

    # def over_scheduling_limit(self, adv_scheduling):
    #     return (self.game.date_time - timezone.now()).days > adv_scheduling

    # def has_visibility(self, user):
    #     return self.role in UserLeagueStatus.objects.get(user, league=self.game.division.league).visibilities.all()

    # def check_apply_status(self, user):
    #     adv_scheduling = self.game.division.league.adv_scheduling_limit
    #     if self.over_scheduling_limit(adv_scheduling):
    #         return {
    #             'status': 'invalid',
    #             'type': 'over_scheduling_limit',
    #             'adv_scheduling_limit': str(adv_scheduling)
    #         }
    #     if self.game.division.league not in user.leagues.accepted():
    #         return {
    #             'status': 'invalid',
    #             'type': 'league'
    #         }
    #     if not self.has_visibility(user):
    #         return {
    #             'status': 'invalid',
    #             'type': 'visibility'
    #         }
    #     if self.application_set.filter(user=user).exists():
    #         return {
    #             'status': 'invalid',
    #             'type': 'duplicate_post'
    #         }
    #     for post in self.game.post_set.all():
    #         if post.application_set.filter(user=user).exists():
    #             return {
    #                 'status': 'invalid',
    #                 'type': 'duplicate_game',
    #                 'post': str(post.application_set.get(user=user).pk)
    #             }
    #     return {
    #         'status': 'valid',
    #         'type': 'success'
    #     }


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

    def is_casted(self):
        return self.get_ordering_queryset().get_min_order() == self.order