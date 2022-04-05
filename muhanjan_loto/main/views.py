from django.shortcuts import render

from .models import Lobby


def index(request):
    lobbies = Lobby.objects.filter(is_active = True)
    return render(request, 'main/index.html', {'title': 'Список лобби', 'lobbies': lobbies})
