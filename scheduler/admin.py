from django.contrib import admin

# Register your models here.
from .models import Room, Professor, Course, TimeSlot

admin.site.register(Room)
admin.site.register(Professor)
admin.site.register(Course)
admin.site.register(TimeSlot)
