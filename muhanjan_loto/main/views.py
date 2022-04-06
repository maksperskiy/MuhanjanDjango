from django.shortcuts import render
from django.db.models import *
from django.http import HttpResponse


from .models import Lobby, Game, Player


def index(request):
    lobbies = Lobby.objects.filter(is_active = True) \
        .annotate(count_users=Count('player'))

    context = {
        'title': 'Список лобби', 
        'lobbies': lobbies
        }
    return render(request, 'main/index.html', context=context)

