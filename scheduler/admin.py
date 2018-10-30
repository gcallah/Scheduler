from django.contrib import admin

# Register your models here.
from .models import Room, Professor, Course, Lesson, CourseCatalog
from .models import ProfessorAvailability, Schedule

admin.site.register(Room)
admin.site.register(Professor)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(CourseCatalog)
admin.site.register(ProfessorAvailability)
admin.site.register(Schedule)
