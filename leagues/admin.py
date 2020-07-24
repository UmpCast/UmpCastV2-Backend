from django.contrib import admin
from .models import League, Division, Role, Level
from ordered_model.admin import OrderedModelAdmin


class LeagueAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'adv_scheduling_limit', 'expiration_date', 'public_access', 'ts_id', 'date_joined')
    list_display_links = ('pk', 'title')
    search_fields = ('title', )
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


class LevelAdmin(OrderedModelAdmin):
    list_display = ('pk', 'title', 'league', 'order', 'move_up_down_links')


admin.site.register(League, LeagueAdmin)
admin.site.register(Division, DivisionAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Level, LevelAdmin)
