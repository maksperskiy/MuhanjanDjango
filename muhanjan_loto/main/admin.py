from csv import list_dialects
from unicodedata import name
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.admin.views.main import ChangeList
from django.contrib.admin.utils import quote

from .forms import LobbyForm
from .models import Game, Lobby, Player


class LobbyChangeList(ChangeList):
    def url_for_result(self, result):
        pk = getattr(result, self.pk_attname)
        game = getattr(result, 'game')
        return f'/{game}/managelobby/{quote(pk)}'


class LobbyAdmin(admin.ModelAdmin):
    list_display = ('name', 'game', 'max_users', 'creator', 'date')
    form = LobbyForm

    def get_queryset(self, request):
        qs = super(LobbyAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(creator=request.user)

    def get_changelist(self, request, **kwargs):
        return LobbyChangeList

    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.creator:
            instance.creator = user
        instance.creator = user
        instance.save()
        form.save_m2m()
        return instance

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='LobbyCreator').exists():
            return True

        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return True


class GameAdmin(admin.ModelAdmin):
    list_display = ('name',)


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('data', 'twitch_name', 'lobby')


admin.site.register(Game, GameAdmin)
admin.site.register(Lobby, LobbyAdmin)
admin.site.register(Player, PlayerAdmin)
