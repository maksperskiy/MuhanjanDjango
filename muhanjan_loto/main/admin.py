from csv import list_dialects
from unicodedata import name
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.admin.views.main import ChangeList
from django.contrib.admin.utils import quote

from .forms import LobbyForm
from .models import Game, Lobby, Player
from loto.models import Card, Barrel, Winner, Stream


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


admin.site.register(Game, GameAdmin)
admin.site.register(Lobby, LobbyAdmin)
admin.site.register(Player)


@admin.action(description='Generate cards')
def make_published(modeladmin, request, queryset):
    print('asdasdasd')

class CardAdmin(admin.ModelAdmin):
    list_display = ['id', 'numbers']
    actions = [make_published]





admin.site.register(Card, CardAdmin)
admin.site.register(Barrel)
admin.site.register(Winner)
admin.site.register(Stream)


def get_app_list(self, request):
    app_dict = self._build_app_dict(request)
    app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

    app_ordering = {
        'main': 1, 
        'auth': 2, 
        'loto': 3
        }
    app_list.sort(key=lambda x: app_ordering[x['app_label']])
    
    for app in app_list:
        if app['app_label'] == 'auth':
            models_ordering = {
                'Users': 1,
                'Groups': 2
            }
            app['models'].sort(key=lambda x: models_ordering[x['name']])
            
        if app['app_label'] == 'main':
            models_ordering = {
                'Games': 1,
                'Lobbies': 2,
                'Players': 3,
            }
            app['models'].sort(key=lambda x: models_ordering[x['name']])
            
        if app['app_label'] == 'loto':
            models_ordering = {
                'Barrels': 1,
                'Winners': 2,
                'Streams': 3,
                'Cards': 4
            }
            app['models'].sort(key=lambda x: models_ordering[x['name']])

    return app_list

admin.AdminSite.get_app_list = get_app_list