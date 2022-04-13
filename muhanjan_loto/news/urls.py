from django.urls import path, re_path
from . import views


urlpatterns = [
    path('ajax/get_all/', views.get_all, name='get_all'),
]   
