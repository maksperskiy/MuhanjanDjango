from csv import list_dialects
from unicodedata import name
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.admin.views.main import ChangeList
from django.contrib.admin.utils import quote

from .forms import NewsForm

from .models import News


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    form = NewsForm


admin.site.register(News, NewsAdmin)
