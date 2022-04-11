from django.urls import path, re_path
from . import views


urlpatterns = [
    path('managelobby/<int:lobby_id>', views.manage_page, name='manage lobby'),
    path('enterlobby/<int:lobby_id>', views.enter_lobby_page, name='enter lobby'),
    path('card/<int:lobby_id>/', views.get_game_card, name='my card'),
    path('managelobby/<int:lobby_id>/get_stream_page/', views.get_stream_page, name='get_stream_page'),

    path('managelobby/<int:lobby_id>/ajax/stop_game/', views.stop_game, name='stop_game'),
    path('managelobby/<int:lobby_id>/ajax/get_stream/', views.get_stream, name='get_stream'),
    path('managelobby/<int:lobby_id>/ajax/add_barrels/', views.get_barrels, name='get_barrels'),
    path('managelobby/<int:lobby_id>/ajax/add_barrel/<int:number>', views.add_barrel, name='add_barrel'),
    path('managelobby/<int:lobby_id>/ajax/remove_barrel/<int:number>/', views.remove_barrel, name='remove_barrel'),


    
]   
