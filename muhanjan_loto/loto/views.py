import json
from django.template.defaulttags import register
from django.http import JsonResponse
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.db.models import *
from django.urls import register_converter
from loto.generator import LotoGenerator

from loto.models import Barrel, Winner, Card, Stream
from main.models import Lobby, Player
# Create your views here.

from functools import wraps


def authors_only(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        creator = any
        if "lobby_id" in kwargs:
            creator = Lobby.objects.get(pk=kwargs["lobby_id"]).creator
        if "player_id" in kwargs:
            creator = Player.objects.get(pk=kwargs["player_id"]).lobby.creator
        if not (request.user.is_superuser or creator == request.user):
            return render(request, 'statuses/403.html')
        return function(request, *args, **kwargs)
    return wrap


def is_active_lobby(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        lobby = any
        if "lobby_id" in kwargs:
            lobby = Lobby.objects.get(pk=kwargs["lobby_id"])
        if "player_id" in kwargs:
            lobby = Player.objects.get(pk=kwargs["player_id"]).lobby
        if not lobby.is_active:
            if "ajax" in request.path:
                response = {
                    'data': "Игра завершена."
                }
                return JsonResponse(response)
            else:
                return render(request, 'statuses/game_stopped.html')
        else:
            return function(request, *args, **kwargs)
    return wrap

@is_active_lobby
@authors_only
def manage_page(request, lobby_id):
    if not Lobby.objects.filter(pk=lobby_id).exists():
        return render(request, 'statuses/404.html')

    lobby = Lobby.objects.get(pk=lobby_id)

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


@is_active_lobby
def enter_lobby_page(request, lobby_id):
    lobby = Lobby.objects.get(pk=lobby_id)
    context = {
        'title': f'Войти в лобби "{lobby.name}"',
        'lobby': lobby,
    }
    return render(request, 'loto/enter_lobby.html', context=context)


@is_active_lobby
def get_game_card(request, lobby_id):
    lobby = Lobby.objects.filter(pk=lobby_id) \
        .annotate(count_users=Count('player')).first()
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
        card = LotoGenerator.generate_loto(player.data)
        context['card'] = card
        return render(request, 'loto/card.html', context=context)

    if lobby.count_users >= lobby.max_users:
        return render(request, 'statuses/lobby_is_full.html')

    employed_cards = Player.objects.filter(lobby=lobby).values('data').all()
    data = Card.objects.filter(~Q(card_id__in=employed_cards)).order_by(
        '?').values('numbers').first()

    player = Player.objects.create(
        twitch_name=name,
        lobby=lobby,
        data=data['numbers'])

    card = LotoGenerator.generate_loto(data['numbers'])
    context['card'] = card

    context['player'] = player
    return render(request, 'loto/card.html', context=context)


@is_active_lobby
def check_win(request, player_id):
    player = Player.objects.get(pk=player_id)

    barrels = Barrel.objects.filter(lobby=player.lobby).values("number").all()
    player_barrels = json.loads(player.data)

    is_win = __check_win(player_barrels, list(
        [el['number'] for el in list(barrels)]))

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


@is_active_lobby
@authors_only
def get_barrels(request, lobby_id):
    lobby = Lobby.objects.get(pk=lobby_id)

    numbers = list(set(map(lambda x: x['number'], list(
        Barrel.objects.filter(lobby=lobby).values('number').all()))))

    response = {
        'numbers': numbers
    }
    return JsonResponse(response)


@is_active_lobby
@authors_only
def add_barrel(request, lobby_id, number):
    lobby = Lobby.objects.get(pk=lobby_id)

    Barrel.objects.create(lobby=lobby, number=number)

    if not Stream.objects.filter(lobby=lobby).exists():
        Stream.objects.create(lobby=lobby, data='')

    new_data = Stream.objects.filter(
        lobby=lobby).values('data').first()['data']
    new_data += ' ' + str(number)
    Stream.objects.filter(lobby=lobby).update(data=new_data)

    response = {
        'number': number
    }
    return JsonResponse(response)


@is_active_lobby
@authors_only
def remove_barrel(request, lobby_id, number):
    lobby = Lobby.objects.get(pk=lobby_id)

    Barrel.objects.filter(lobby=lobby, number=number).all().delete()

    new_data = Stream.objects.filter(lobby=lobby).values('data').first()[
        'data'].removesuffix(' ' + str(number))
    Stream.objects.filter(lobby=lobby).update(data=new_data)

    response = {
        'number': number
    }
    return JsonResponse(response)


@authors_only
def get_winners(request, lobby_id):
    winners_list = []
    if Winner.objects.filter(player__lobby_id=lobby_id).exists():
        winners = list(Winner.objects.filter(player__lobby_id=lobby_id).all())
        [winners_list.append(
            {
                "player_id": el.player.pk,
                "player_name": el.player.twitch_name,
                "is_submited": el.is_submited
            }
        ) for el in winners]
    response = {
        'winners': winners_list
    }
    return JsonResponse(response)


@authors_only
def submit_winner(request, player_id):
    player = Player.objects.get(pk=player_id)
    winner = Winner.objects.filter(player=player).update(is_submited=True)

    new_data = Stream.objects.filter(lobby_id=player.lobby_id).values(
        'data').first()['data'] + ' Победитель: ' + player.twitch_name
    Stream.objects.filter(lobby=player.lobby).update(data=new_data)

    response = {
        'winner': winner
    }
    return JsonResponse(response)


def get_stream_page(request, lobby_id):
    lobby = Lobby.objects.get(pk=lobby_id)
    context = {
        "lobby": lobby
    }
    return render(request, 'loto/stream_page.html', context=context)


def get_stream(request, lobby_id):
    lobby = Lobby.objects.filter(pk=lobby_id).first()

    stream = []
    if Stream.objects.filter(lobby=lobby).exists():
        stream = Stream.objects.get(lobby=lobby).data

    response = {
        'data': stream
    }
    return JsonResponse(response)


@is_active_lobby
@authors_only
def stop_game(request, lobby_id):
    lobby = Lobby.objects.get(pk=lobby_id)

    lobby.is_active = False
    lobby.save()

    return render(request, 'statuses/game_stopped.html')
