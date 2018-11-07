from django import forms
from django.db import models
from django.forms import ModelForm

# Create your models here.

# we're going to need tables for rooms, courses, professors, and...?



class Room(models.Model):
    rname = models.CharField(max_length=128, default="")
    capacity = models.IntegerField()
    rtype = models.CharField(max_length=128, default="Lecture")
    building = models.CharField(max_length=128, default="", blank=True)

    def __str__(self):
        return self.rname

class Professor(models.Model):
	pname = models.CharField(max_length=128, blank=False)

class Course(models.Model):
	isSelected=models.BooleanField(default=False, primary_key=True)
	cname = models.CharField(max_length=128, blank=False)
	capacity = models.IntegerField(default = 0)

	def __str__(self):
		return self.cname

class TimeSlot(models.Model):
	rname = models.ForeignKey(Room, on_delete=models.CASCADE)
	cname = models.ForeignKey(Course, on_delete=models.CASCADE)
	start_time = models.IntegerField(default = 0)
	end_time = models.IntegerField(default = 0)
	days = models.CharField(max_length=128)

	def __unicode__(self):
		return self.cname

class Lesson(models.Model):
	cname = models.ForeignKey(Course, on_delete=models.CASCADE)
	ctype = models.CharField(max_length=128)
	rtype = models.CharField(max_length=128)
	length = models.IntegerField()

#Used to save form submissions. Each "Schedule" object includes a course name, room, and number of students.
class Schedule(models.Model):
	cname = models.CharField(max_length=128, blank=False)
	room = models.CharField(max_length=128, blank=False)
	numStudents=models.IntegerField(default=0, blank=False)

