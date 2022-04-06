from django.urls import path
from . import views


urlpatterns = [
    path('managelobby/<int:pk>', views.manage_page, name='manage lobby')
]
