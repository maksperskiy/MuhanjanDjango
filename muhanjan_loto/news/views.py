import base64
from django.http import JsonResponse
from django.shortcuts import render

from .models import News


def get_all(request):
    news = list(News.objects.all())
    data = [{
            "title": el.title,
            "text": el.text,
            "image": el.image,
            "date": el.date
            }
            for el in news]
    response = {
        'news': data
    }
    return JsonResponse(response)
