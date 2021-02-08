from django.db import models
from .game import Game
from .gamer import Gamer

class Event(models.Model):
	event_time = models.DateTimeField(auto_now_add=True)
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	location = models.CharField(max_length=255)
	scheduler = models.ForeignKey(Gamer, on_delete=models.CASCADE)