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


def add_filter(request, kwargs, get_name, kwarg_name):
    courses = request.GET.getlist(get_name)

    for course in courses:
        if course != '':
            kwargs.append(course)


def schedule(request):
    if (request.method == 'POST'):
        form_data = request.POST
        courses = {}

        # Returns a dictionary of courses and the number of sections to schedule for each course
        # If number of sections is 0, then course name does not get added to dictionary
        for key, value in form_data.items():
            if (key != 'csrfmiddlewaretoken' and int(value) != 0):
                courses[key] = value
        
        all_courses = Course.objects.filter(cname__in=list(courses.keys())).order_by('-capacity')
        all_rooms = Room.objects.all().order_by('-capacity')
        scheduled_courses = make_schedule(all_courses, all_rooms)
        unscheduled_courses = get_unscheduled_course(
            all_courses, scheduled_courses)
        return render(request, 'schedule.html', {
            'dictionary': scheduled_courses, 'unscheduled': unscheduled_courses})


def make_schedule(all_courses, all_rooms):
    scheduled_courses = {}
    for course in all_courses:
        for room in all_rooms:
            if (room.rname not in scheduled_courses and course.cname
                    not in scheduled_courses.values()):
                if course.capacity < room.capacity:
                    scheduled_courses[room.rname] = course.cname
    return scheduled_courses


def get_unscheduled_course(all_courses, scheduled_courses):
    unscheduled_courses = []
    for course in all_courses:
        if course.cname not in scheduled_courses.values():
            unscheduled_courses.append(course.cname)
    return unscheduled_courses
