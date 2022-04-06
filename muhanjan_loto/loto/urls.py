from django.urls import path
from . import views


urlpatterns = [
    path('managelobby/<int:lobby_id>', views.manage_page, name='manage lobby')
]
