from django.contrib import admin
from .models import UmpCastNotification, LeagueNotification, GameNotification, ApplicationNotification


class UmpCastNotificationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'notification_date_time', 'subject')
    list_display_links = ('pk', )
    search_fields = ('pk', 'user', 'subject')
    list_per_page = 25


class LeagueNotificationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'league', 'notification_date_time', 'subject')
    list_display_links = ('pk', )
    search_fields = ('pk', 'subject', 'league')
    list_per_page = 25


class GameNotificationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'game', 'notification_date_time', 'subject')
    list_display_links = ('pk', )
    search_fields = ('pk', 'subject', 'game')
    list_per_page = 25


class ApplicationNotificationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'application', 'notification_date_time', 'subject')
    list_display_links = ('pk', )
    search_fields = ('pk', 'subject', 'application')
    list_per_page = 25


admin.site.register(UmpCastNotification, UmpCastNotificationAdmin)
admin.site.register(LeagueNotification, LeagueNotificationAdmin)
admin.site.register(GameNotification, GameNotificationAdmin)
admin.site.register(ApplicationNotification, ApplicationNotificationAdmin)
