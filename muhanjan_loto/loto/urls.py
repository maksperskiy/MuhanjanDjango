from django.urls import path, re_path
from . import views


urlpatterns = [
    path('managelobby/<int:lobby_id>', views.manage_page, name='manage lobby'),
    path('enterlobby/<int:lobby_id>', views.enter_lobby_page, name='enter lobby'),
    path('card/<int:lobby_id>/', views.get_game_card, name='my card'),

    path('managelobby/<int:lobby_id>/', views.stop_game, name='stop_game'),
    path('managelobby/<int:lobby_id>/', views.get_stream, name='get_stream'),
    path('managelobby/<int:lobby_id>/', views.add_barrel, name='add_barrel'),


    
]   
