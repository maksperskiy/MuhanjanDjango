import json
from django.http import JsonResponse
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from loto.models import Barrel, Winner, Card, Stream
from main.models import Lobby, Player
# Create your views here.

def manage_page(request, lobby_id):
    lobby = Lobby.objects.filter(pk=lobby_id).first()

    if not (request.user.is_superuser or lobby.creator == request.user):
        raise PermissionDenied

    barrels = Barrel.objects.filter(lobby=lobby).values('number').all()
    winners = Winner.objects.filter(player__lobby=lobby).values('player').all()
    context = {
        'title': 'Управление лобби Лото',
        'lobby': lobby,
        'barrels': barrels,
        'winners': winners
        }

    return render(request, 'loto/manage_lobby.html', context=context)

def enter_lobby_page(request, lobby_id):
    lobby = Lobby.objects.filter(pk=lobby_id).first()
    context = {
        'title': 'Войти в лобби "{lobby.name}"',
        'lobby': lobby,
    }
    return render(request, 'loto/enter_lobby.html', context=context)

def get_game_card(request, lobby_id, name, password):
    lobby = Lobby.objects.filter(pk=lobby_id).first()
    
    if password != lobby.password:
        raise PermissionDenied
    
    context = {
        'title': 'Лото "{lobby.name}"',
        'lobby': lobby,
    }
    if Player.objects.filter(lobby=lobby, name=name).exists():
        player = Player.objects.filter(lobby=lobby, name=name).first()
        context['player'] = player
        return render(request, 'loto/card.html', context=context)

    employed_cards = Player.objects.filter(lobby=lobby).values('data').all()
    data = Card.objects.filter(~Q(data__in=employed_cards)).order_by('?').values('data').first()

    data = json.loads(data)
    player = Player.objects.create(
        twitch_name=name, 
        lobby=lobby, 
        data=data)
    
    context['player'] = player
    return render(request, 'loto/card.html', context=context)

def is_win(request, player_id):
    pass

def add_barrel(request, lobby_id, number):
    pass
