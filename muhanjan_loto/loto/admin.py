from django.contrib import admin

from .generator import LotoGenerator
# Register your models here.

from .models import Card, Barrel, Winner, Stream


@admin.action(description='Generate cards')
def generate_cards(modeladmin, request, queryset):
    cards = [Card(card_id=key, numbers=value) for key, value in LotoGenerator.generate_lotteries().items()]
    Card.objects.bulk_create(cards)

class CardAdmin(admin.ModelAdmin):
    list_display = ['card_id', 'numbers']
    actions = [generate_cards]

    def get_ordering(self, request):
        return ['card_id']


def get_app_list(self, request):
    app_dict = self._build_app_dict(request)
    app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

    app_ordering = {
        'main': 1,
        'auth': 2,
        'news': 3,
        'loto': 4,
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

admin.site.register(Card, CardAdmin)
admin.site.register(Barrel)
admin.site.register(Winner)
admin.site.register(Stream)
