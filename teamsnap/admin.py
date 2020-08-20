from django.contrib import admin

from .models import TeamSnapNote, TeamSnapNoteItem


class TeamSnapNoteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'league', 'date_time', 'note_type')
    list_display_links = ('pk',)
    search_fields = ('pk', 'league', 'note_type')
    list_per_page = 25


class TeamSnapNoteItemAdmin(admin.ModelAdmin):
    list_display = ('pk', 'teamsnap_note', 'note')
    list_display_links = ('pk',)
    search_fields = ('pk',)
    list_per_page = 25


admin.site.register(TeamSnapNote, TeamSnapNoteAdmin)
admin.site.register(TeamSnapNoteItem, TeamSnapNoteItemAdmin)
