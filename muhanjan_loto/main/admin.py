from django.contrib import admin
from .models import Game, Lobby, Player


class LobbyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'max_users')



admin.site.register(Game)
admin.site.register(Lobby)
admin.site.register(Player)
