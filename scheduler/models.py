from django.db import models
from datetime import datetime

DAYS_OF_WEEK = (
    ("Monday", 'Monday'),
    ("Tuesday", 'Tuesday'),
    ("Wednesday", 'Wednesday'),
    ("Thursday", 'Thursday'),
    ("Friday", 'Friday'),
    ("Saturday", 'Saturday'),
    ("sunday", 'Sunday'),
)


class Room(models.Model):
    rname = models.CharField(max_length=128, default="")
    capacity = models.IntegerField()
    rtype = models.CharField(max_length=128, default="Lecture")
    building = models.CharField(max_length=128, default="", blank=True)

    def __str__(self):
        return self.rname


class Course(models.Model):
    cname = models.CharField(max_length=128, blank=False)
    pname = models.CharField(default="", max_length=128, blank=False)
    capacity = models.IntegerField(default=0)

    def __str__(self):
        return self.cname


class Feedback(models.Model):
    fname = models.CharField("First Name", max_length=20, blank=True)
    lname = models.CharField("Last Name", max_length=20, blank=True)
    email_address = models.CharField(
        "Email Address", max_length=128, blank=True)
    comments = models.CharField("Comments", max_length=500, blank=True)
