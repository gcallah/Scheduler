from django.db import models
from datetime import datetime

DAYS_OF_WEEK = (
    ("M", 'Monday'),
    ("Tu", 'Tuesday'),
    ("W", 'Wednesday'),
    ("Th", 'Thursday'),
    ("F", 'Friday'),
    ("S", 'Saturday'),
    ("MW", 'Monday & Wednesday'),
    ("TuTh", 'Tuesday & Thursday'),
)

TIMES = (
    ("8", "8"), ("9", "9"), ("10", "10"), ("11", "11"), ("12", "12"),
    ("13", "13"), ("14", "14"), ("15", "15"), ("16", "16"), ("17", "17"),
    ("18", "18"),("19", "19"), ("20", "20"), ("21", "21"), ("22", "22"),
)


class Room(models.Model):
    rname = models.CharField(max_length=128, default="")
    capacity = models.IntegerField()
    rtype = models.CharField(max_length=128, default="Lecture")
    building = models.CharField(max_length=128, default="", blank=True)
    days = models.ManyToManyField('Day')
    times = models.ManyToManyField('Time')

    def __str__(self):
        return self.rname


class Course(models.Model):
    cname = models.CharField(max_length=128, blank=False)
    pname = models.CharField(default="", max_length=128, blank=False)
    capacity = models.IntegerField(default=0)
    days = models.ManyToManyField('Day')
    times = models.ManyToManyField('Time')
    duration = models.IntegerField(default=1)

    def __str__(self):
        return self.cname


class Time(models.Model):
    times = models.CharField(max_length=2, choices=TIMES)

    def __str__(self):
        return self.times


class Request(models.Model):
    date_time = models.CharField(max_length=128, default="")
    scheduled = models.TextField(default="{}", blank=False)
    unscheduled = models.TextField(default="{}", blank=False)

    def __str__(self):
        return str(self.date_time)


class Day(models.Model):
    days = models.CharField(    
        default="Monday", max_length=9, choices=DAYS_OF_WEEK)

    def __str__(self):
        return self.days


class Feedback(models.Model):
    fname = models.CharField("First Name", max_length=20, blank=True)
    lname = models.CharField("Last Name", max_length=20, blank=True)
    email_address = models.CharField(
        "Email Address", max_length=128, blank=True)
    comments = models.CharField("Comments", max_length=500, blank=True)
