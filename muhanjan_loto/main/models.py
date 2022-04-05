from datetime import datetime
from django.conf import settings
from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=50)
    max_users = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class Lobby(models.Model):
    name = models.CharField(max_length=50)
    max_users = models.IntegerField(default=1)
    date = models.DateTimeField(default=datetime.now())
    is_active = models.BooleanField(default=True)
    password = models.CharField(max_length=5, blank=True, null=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        default=None, blank=True, null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Lobbies'
        ordering = ['-id']


class Player(models.Model):
    twitch_name = models.CharField(max_length=50)
    data = models.TextField()
    lobby = models.ForeignKey(Lobby, on_delete=models.CASCADE)
    
    class Meta():
        index_together = [['lobby']]
