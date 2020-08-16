from django.contrib import admin
from .models import Game, Post, Application


class GameAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'date_time', 'division', 'is_active', 'location', 'description')
    list_display_links = ('pk', 'title')
    search_fields = ('pk', 'title')
    list_per_page = 25

    def save_model(self, request, obj, form, change):
        update_fields = []
        if change:
            for key, value in form.cleaned_data.items():
                # True if something changed in model
                if value != form.initial[key]:
                    update_fields.append(key)
            obj.save(update_fields=update_fields)
        else:
            obj.save()
            

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
