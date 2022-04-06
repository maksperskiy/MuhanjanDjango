from django.urls import path
from . import views


urlpatterns = [
    path('managelobby/<int:lobby_id>', views.manage_page, name='manage lobby'),
    path('enterlobby/<int:lobby_id>', views.enter_lobby_page, name='enter lobby'),
    path('card/<int:lobby_id>/', views.get_game_card, name='my card'),
]   
