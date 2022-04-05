from django.shortcuts import render
from django.db.models import *


from .models import Lobby, Game, Player


def index(request):
    lobbies = Lobby.objects.filter(is_active = True) \
        .annotate(count_users=Count('player'))
    return render(request, 'main/index.html', {'title': 'MuhanJan', 'lobbies': lobbies})
