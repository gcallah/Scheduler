from django.contrib import admin

# Register your models here.
from .models import Room, Course, Feedback

admin.site.register(Room)
admin.site.register(Course)
admin.site.register(Feedback)
