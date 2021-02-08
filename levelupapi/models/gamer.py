from django.db import models
from django.db.models.fields.related import OneToOneField
from django.contrib.auth.models import User

class Gamer(models.Model):
	bio = models.CharField(max_length=255)
	user = OneToOneField(User, on_delete=models.CASCADE)