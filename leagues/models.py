from django.db import models
from django.utils.timezone import now
from datetime import datetime, timedelta
from django.contrib.postgres.fields import JSONField
from ordered_model.models import OrderedModel
from django.core.validators import MinValueValidator


def set_league_expiration_date():
    return now() + timedelta(days=14)


def set_apply_league_expiration_date():
    return now() + timedelta(days=7)


class LeagueRelatedModelManager(models.Manager):
    """Custom RelatedModelManager to filter leagues by through UserLeagueStatus model"""

    use_for_related_fields = True

    def accepted(self):
        return self.get_queryset().filter(userleaguestatus__request_status='accepted')

    def pending(self):
        return self.get_queryset().filter(userleaguestatus__request_status='pending')

    def rejected(self):
        return self.get_queryset().filter(userleaguestatus__request_status='rejected')


class League(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=1028, null=True, blank=True)
    league_picture = models.ImageField(
        upload_to='league_pics/%Y/%m/', null=True, blank=True)
    date_joined = models.DateTimeField(default=now)
    expiration_date = models.DateTimeField(default=set_league_expiration_date)
    public_access = models.BooleanField(default=False)
    can_apply = models.BooleanField(default=True)
    email = models.EmailField(max_length=64, blank=True,  null=True)
    website_url = models.CharField(max_length=64, blank=True, null=True)

    # how many days in advance games are scheduled
    adv_scheduling_limit = models.IntegerField(
        default=30, validators=[MinValueValidator(0)])
    # how many days in advance games can be canneled
    cancellation_period = models.IntegerField(
        default=2, validators=[MinValueValidator(0)])

    # defaults
    default_max_casts = models.IntegerField(
        default=0, validators=[MinValueValidator(0)])
    default_max_backups = models.IntegerField(
        default=0, validators=[MinValueValidator(0)])

    # uls m2m custom manager
    objects = LeagueRelatedModelManager()

    # team snap fields
    api_key = models.CharField(
        default="", max_length=128, blank=True, null=True)
    is_synced = models.BooleanField(default=False)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return self.title


class Division(OrderedModel):
    title = models.CharField(max_length=32)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    order_with_respect_to = 'league'

    # team snap fields
    ts_id = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Role(OrderedModel):
    title = models.CharField(max_length=32)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    order_with_respect_to = 'division'

    def __str__(self):
        return ' '.join([self.division.title, self.title])


class Level(OrderedModel):
    title = models.CharField(max_length=32, null=False, blank=False)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    visibilities = models.ManyToManyField(Role, blank=True)
    order_with_respect_to = 'league'
