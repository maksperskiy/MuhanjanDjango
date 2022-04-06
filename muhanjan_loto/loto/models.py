from datetime import datetime
import numbers
from django.conf import settings
from django.db import models
from main.models import Lobby, Player


class Card(models.Model):
    card_id = models.IntegerField(blank=True, null=True)
    numbers = models.CharField(max_length=50)

    def __str__(self):
        return self.numbers
        
    class Meta():
        index_together = [['card_id']]


class Barrel(models.Model):
    number = models.IntegerField()
    lobby = models.ForeignKey(Lobby, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.number

    class Meta():
        index_together = [['lobby']]


class Winner(models.Model):
    is_submited = models.BooleanField(default=False)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    
    class Meta():
        index_together = [['player']]


class Stream(models.Model):
    data = models.TextField()
    lobby = models.ForeignKey(Player, on_delete=models.CASCADE)
    
    class Meta():
        index_together = [['lobby']]