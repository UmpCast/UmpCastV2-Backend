from datetime import timedelta

from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone

from games.models import Application, Game


class BaseNotification(models.Model):
    """
    Used to ensure that all notification types have the same structure
    """
    notification_date_time = models.DateTimeField(default=timezone.now)
    subject = models.CharField(max_length=64, null=True, blank=True)
    message = models.CharField(max_length=256)

    def save(self, *args, **kwargs):
        if self.subject:
            self.subject = self.subject[:64]
        self.message = self.message[:256]
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['-notification_date_time']


class UmpCastNotification(BaseNotification):
    """
    UmpCast Level Notification
    """


class LeagueNotification(BaseNotification):
    """
    League Level Notifications. External Notifications sent immediately
    """
    league = models.ForeignKey('leagues.League', on_delete=models.CASCADE)


class GameNotification(BaseNotification):
    """
    Game Level Notifications. Reminder notifications sent using Chronschedule. Changes sent immediately
    """
    game = models.ForeignKey('games.Game', on_delete=models.CASCADE)
    was_reminded = models.BooleanField(default=False)


class ApplicationNotification(BaseNotification):
    """
    Application Level Notifications. External Notifications sent immediately
    """
    application = models.ForeignKey(
        'games.Application', on_delete=models.CASCADE)


ADVANCED_NOTIFICATION_DAYS = 1


def game_handle_creation(instance):
    if instance.is_active:
        GameNotification.objects.create(
            game=instance,
            was_reminded=False,
            notification_date_time=instance.date_time -
            timedelta(days=ADVANCED_NOTIFICATION_DAYS),
            subject=f"{instance.title} Game Reminder",
            message=f"Reminder for {instance.title}: Date Time {str(instance.date_time)}, Location {instance.location}"
        )


def game_handle_update(instance, **kwargs):
    verbose_dict = {
        'date_time': 'Date and Time',
        'location': 'Location',
        'description': 'Details'
    }
    game_dict = {
        'game': instance,
        'was_reminded': True,
        'notification_date_time': timezone.now()
    }

    if kwargs['update_fields'] is None:
        print("It doesn't appear that any fields were updated")
        return

    fields = ('title', 'date_time', 'location', 'description')
    for field in fields:
        if field in kwargs['update_fields'] and instance.is_active:
            GameNotification.objects.create(**dict(game_dict,
                                                   subject=f"{instance.title} {verbose_dict.get(field)} updated",
                                                   message=f"{verbose_dict.get(field)} for {instance.title} has been updated to: {str(getattr(instance,field))}"))

    if 'is_active' in kwargs['update_fields']:
        if instance.is_active:
            GameNotification.objects.create(**dict(game_dict,
                                                   subject=f"{instance.title} uncancelled",
                                                   message=f"{instance.title} has been uncancelled. Here are the details: Date Time {str(instance.date_time)}, Location {instance.location}"))
        else:
            GameNotification.objects.create(**dict(game_dict,
                                                   subject=f"{instance.title} cancelled",
                                                   message=f"{instance.title} has been cancelled"))

# API Create Endpoint, Admin Create/Update, TS Create/Update


def game_notification_receiver(sender, instance, *args, **kwargs):
    if kwargs['created']:
        game_handle_creation(instance)
    else:
        # update_fields (title, date_time, is_active, location, description)
        game_handle_update(instance, **kwargs)


post_save.connect(game_notification_receiver, sender=Game)


def is_casted(application):
    return application.post.application_set.get_min_order() == application.order


def notify_application(application):
    app_dict = {
        'application': application,
        'notification_date_time': timezone.now(),
    }
    if is_casted(application):
        ApplicationNotification.objects.create(**dict(app_dict,
                                                      subject=f"Casted for {application.post.game.title}",
                                                      message=f"You are currently now casted for {application.post.game.title}"))
    else:
        ApplicationNotification.objects.create(**dict(app_dict,
                                                      subject=f"Backup for {application.post.game.title}",
                                                      message=f"You are currently now a backup for {application.post.game.title}"))


def application_notification_receiver(sender, instance, *args, **kwargs):
    # check the application set for applications which require updates
    if kwargs['created']:
        notify_application(instance)
    if not kwargs['update_fields'] is None and 'order' in kwargs['update_fields']:
        if is_casted(instance):
            notify_application(instance)
            if instance.next():
                notify_application(instance.next())
        else:
            notify_application(instance)
            casted = instance.get_ordering_queryset().below_instance(instance).first()
            notify_application(casted)


post_save.connect(application_notification_receiver, sender=Application)


def print_game_notification(sender, instance, *args, **kwargs):
    pass
    # print(instance)


post_save.connect(print_game_notification, sender=GameNotification)


def print_application_notification(sender, instance, *args, **kwargs):
    pass
    # print(instance)


post_save.connect(print_application_notification,
                  sender=ApplicationNotification)
