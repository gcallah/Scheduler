from django.shortcuts import render
from scheduler.forms import FeedbackForm
from scheduler.forms import CourseForm
from .models import Course
from .models import Room

site_hdr = "Course Scheduler"


def index(request):
    form = CourseForm
    course_list = Course.objects.all().order_by('cname')

    context = {'course_list': course_list, 'form': form, 'header': site_hdr}

    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html', {'header': site_hdr})


# This feedback form old and will be redone using a model form.
def feedback(request):
    form_class = FeedbackForm

    return render(request, 'feedback.html', {'form': form_class})


def requirements(request):
    return render(request, 'requirements.html', {'header': site_hdr})


def schedule(request):

    all_courses = Course.objects.all().order_by('-capacity')
    all_rooms = Room.objects.all().order_by('-capacity')

    scheduled_rooms = {}
    for course in all_courses:
        for room in all_rooms:
            if (room.rname not in scheduled_rooms and course.cname
                    not in scheduled_rooms.values()):
                if course.capacity < room.capacity:
                    scheduled_rooms[room.rname] = course.cname

    # print(scheduled_rooms)
    return render(request, 'schedule.html', {'dictionary': scheduled_rooms})
