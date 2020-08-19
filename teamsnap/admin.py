from django.contrib import admin

from .models import TeamSnapNote, TeamSnapNoteItem


class TeamSnapNoteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'league', 'date_time')
    list_display_links = ('pk',)
    search_fields = ('pk', 'league')
    list_per_page = 25


class TeamSnapNoteItemAdmin(admin.ModelAdmin):
    list_display = ('pk', 'teamsnap_note', 'note')
    list_display_links = ('pk',)
    search_fields = ('pk',)
    list_per_page = 25


admin.site.register(TeamSnapNote, TeamSnapNoteAdmin)
admin.site.register(TeamSnapNoteItem, TeamSnapNoteItemAdmin)
