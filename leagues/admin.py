from django.contrib import admin
from .models import League, Division, Role, Level
from ordered_model.admin import OrderedModelAdmin


class LeagueAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'adv_scheduling_limit',
                    'expiration_date', 'public_access', 'date_joined', 'api_key')
    list_display_links = ('pk', 'title')
    search_fields = ('title', )
    list_per_page = 25


class DivisionAdmin(OrderedModelAdmin):
    list_display = ('pk', 'title', 'league', 'ts_id', 'move_up_down_links')
    list_display_links = ('pk', 'title')
    search_fields = ('title', )
    list_per_page = 25


class RoleAdmin(OrderedModelAdmin):
    list_display = ('pk', 'title', 'division', 'move_up_down_links')
    list_display_links = ('pk', 'title')
    search_fields = ('title', )
    list_per_page = 25


class LevelAdmin(OrderedModelAdmin):
    list_display = ('pk', 'title', 'league', 'order', 'move_up_down_links')


admin.site.register(League, LeagueAdmin)
admin.site.register(Division, DivisionAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Level, LevelAdmin)
