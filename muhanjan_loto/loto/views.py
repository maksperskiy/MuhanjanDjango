import json
from django.http import JsonResponse
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from loto.models import Barrel, Winner, Card, Stream
from main.models import Lobby, Player
# Create your views here.

def manage_page(request, lobby_id):
    lobby = Lobby.objects.get(pk=lobby_id)

    if not (request.user.is_superuser or lobby.creator == request.user):
        return render(request, 'statuses/403.html')
    
    if not Stream.objects.filter(lobby=lobby).exists():
        Stream.objects.create(lobby=lobby, data='')

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
    lobby = Lobby.objects.get(pk=lobby_id)
    context = {
        'title': f'Войти в лобби "{lobby.name}"',
        'lobby': lobby,
    }
    return render(request, 'loto/enter_lobby.html', context=context)

def get_game_card(request, lobby_id):
    lobby = Lobby.objects.get(pk=lobby_id)
    
    if lobby.password:
        if not 'password' in request.GET:
            raise PermissionDenied

        if request.GET['password'] != lobby.password:
            raise PermissionDenied
    
    if not 'twitch_name' in request.GET:
        raise PermissionDenied

    name = request.GET['twitch_name']
    context = {
        'title': 'Лото "{lobby.name}"',
        'lobby': lobby,
    }
    if Player.objects.filter(lobby=lobby, twitch_name=name).exists():
        player = Player.objects.filter(lobby=lobby, twitch_name=name).first()
        context['player'] = player
        return render(request, 'loto/card.html', context=context)

    employed_cards = Player.objects.filter(lobby=lobby).values('data').all()
    data = Card.objects.filter(~Q(card_id__in=employed_cards)).order_by('?').values('numbers').first()

    player = Player.objects.create(
        twitch_name=name, 
        lobby=lobby, 
        data=data['numbers'])
    
    context['player'] = player
    return render(request, 'loto/card.html', context=context)

def check_win(request, player_id):
    player = Player.objects.get(pk=player_id)

    if not player.lobby.is_active:
        return render(request, 'statuses/game_stopped.html')
        
    barrels = Barrel.objects.filter(lobby=player.lobby).all()
    player_barrels = json.loads(player.data)

    is_win = __check_win(player_barrels, barrels)
    
    if is_win:
        Winner.objects.create(player=player)

    response = {
        'is_win': is_win
    }
    return JsonResponse(response)

def __check_win(player_barrels, barrels):
    for el in player_barrels:
        if el not in barrels:
            return False
    return True

def add_barrel(request, lobby_id, number):
    lobby = Lobby.objects.get(pk=lobby_id)

    if not lobby.is_active:
        return render(request, 'statuses/game_stopped.html')

    Barrel.objects.create(lobby=lobby, number=number)
    
    new_data = Stream.objects.filter(lobby=lobby).values('data').first() + ' ' + number
    Stream.objects.filter(lobby=lobby).update(data=new_data)

    response = {
        'number': number
    }
    return JsonResponse(response)
    

def get_winners(request, lobby_id):
    lobby = Lobby.objects.get(pk=lobby_id)

    winners = Winner.objects.filter(player__lobby=lobby).all()
    
    response = {
        'winners': winners
    }
    return JsonResponse(response)

def submit_winner(request, player_id):
    player = Player.objects.get(pk=player_id)
    winner = Winner.objects.filter(player=player).update(is_submited=True)

    new_data = Stream.objects.filter(lobby=player.lobby).values('data').first() + ' ' + player.twitch_name
    Stream.objects.filter(lobby=player.lobby).update(data=new_data)

    response = {
        'winner': winner
    }
    return JsonResponse(response)

def get_stream(request, lobby_id):
    lobby = Lobby.objects.filter(pk=lobby_id).first()
    
    if not lobby.is_active:
        return render(request, 'statuses/game_stopped.html')

    stream = Stream.objects.get(lobby=lobby)

    response = {
        'data': stream.data
    }
    return JsonResponse(response)

def stop_game(request, lobby_id):
    lobby = Lobby.objects.get(pk=lobby_id)

    if not lobby.is_active:
        return render(request, 'statuses/game_stopped.html')

    lobby.is_active = False
    lobby.save()

    return render(request, 'statuses/game_stopped.html')
