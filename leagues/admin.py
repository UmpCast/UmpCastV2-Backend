from django.contrib import admin
from .models import ApplyLeagueCode, League, Division, Role


class LeagueAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'adv_scheduling_limit', 'expiration_date', 'public_access', 'ts_id', 'date_joined')
    list_display_links = ('pk', 'title')
    search_fields = ('title', )
    list_per_page = 25


class ApplyLeagueCodeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'code', 'league', 'expiration_date')
    list_display_links = ('pk', 'code')
    search_fields = ('code', )
    list_per_page = 25


class DivisionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'league', 'ts_id')
    list_display_links = ('pk', 'title')
    search_fields = ('title', )
    list_per_page = 25


class RoleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'division')
    list_display_links = ('pk', 'title')
    search_fields = ('title', )
    list_per_page = 25


admin.site.register(League, LeagueAdmin)
admin.site.register(ApplyLeagueCode, ApplyLeagueCodeAdmin)
admin.site.register(Division, DivisionAdmin)
admin.site.register(Role, RoleAdmin)

