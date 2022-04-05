from django.contrib import admin
from django.contrib.auth.models import Group


from .forms import LobbyForm
from .models import Game, Lobby, Player


class LobbyAdmin(admin.ModelAdmin):
    list_display = ('name', 'game', 'max_users', 'creator', 'date')
    form = LobbyForm
    
    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.creator:
            instance.creator = user
        instance.creator = user
        instance.save()
        form.save_m2m()
        return instance


class GameAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Game, GameAdmin)
admin.site.register(Lobby, LobbyAdmin)
admin.site.register(Player)
admin.site.unregister(Group)
