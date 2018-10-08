
from django.db import models

# Create your models here.

# we're going to need tables for rooms, courses, professors, and...?

class Room(models.Model):
    name = models.CharField(max_length=128)
    building = models.CharField(max_length=128, default="", blank=True)
    capacity = models.IntegerField()
