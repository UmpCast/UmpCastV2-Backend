from django.contrib import admin
from .models import User, UserLeagueStatus


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'first_name', 'last_name', 'date_joined')
    list_display_links = ('pk', 'email')
    search_fields = ('email', 'first_name', 'last_name')
    list_per_page = 25


class UserLeagueStatusAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'league', 'date_pending', 'date_joined', 'request_status', 'max_casts', 'max_backups')
    list_display_links = ('pk',)
    search_fields = ('pk', 'user', 'league')
    list_per_page = 25


admin.site.register(User, UserAdmin)
admin.site.register(UserLeagueStatus, UserLeagueStatusAdmin)
