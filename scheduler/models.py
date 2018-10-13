
from django.db import models

# Create your models here.

# we're going to need tables for rooms, courses, professors, and...?

class Room(models.Model):
    rname = models.CharField(max_length=128, default="")
    rtype = models.CharField(max_length=128, default="Lecture")
    building = models.CharField(max_length=128, default="", blank=True)
    capacity = models.IntegerField()

class Professor(models.Model):
	pname = models.CharField(max_length=128, blank=False)

class Course(models.Model):
	cname = models.CharField(max_length=128, blank=False)

class Lesson(models.Model):
	cname = models.ForeignKey(Course, on_delete=models.CASCADE)
	ctype = models.CharField(max_length=128)
	rtype = models.CharField(max_length=128)
	length = models.IntegerField()

class CourseCatalog(models.Model):
	cname = models.ForeignKey(Course, on_delete=models.CASCADE)
	pname = models.ForeignKey(Professor, on_delete=models.CASCADE)

class ProfessorAvailability(models.Model):
	pname = models.ForeignKey(Professor, on_delete=models.CASCADE)
	start_time = models.TimeField()
	end_time = models.TimeField()
	day_of_week = models.CharField(max_length=128)