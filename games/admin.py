from django.contrib import admin
from .models import Game, Post, Application


class GameAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'date_time', 'division', 'is_active', 'location', 'description')
    list_display_links = ('pk', 'title')
    search_fields = ('pk', 'title')
    list_per_page = 25


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'game', 'role')
    list_display_links = ('pk',)
    list_per_page = 25


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'post', 'user', 'comments')
    list_display_links = ('pk', )
    list_per_page = 25


admin.site.register(Game, GameAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Application, ApplicationAdmin)
