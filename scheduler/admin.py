from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Room)
admin.site.register(Professor)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(CourseCatalog)
admin.site.register(ProfessorAvailability)
admin.site.register(Schedule)