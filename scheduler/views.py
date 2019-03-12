from django.shortcuts import render
from scheduler.forms import FeedbackForm
from .schedule import sched
from .models import Course
from .organize_data import organize
import json

site_hdr = "Course Scheduler"
max_sections = 5


def index(request):
    course_list = Course.objects.all().order_by('cname')
    context = {
        'course_list': course_list,
        'header': site_hdr,
        'max_sections': range(max_sections + 1)
    }

    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html', {'header': site_hdr})


# This feedback form old and will be redone using a model form.
def feedback(request):
    form = FeedbackForm(request.POST)

    if form.is_valid():
        form.save()

    return render(request, 'feedback.html', {'header': site_hdr, 'form': form})


def requirements(request):
    return render(request, 'requirements.html', {'header': site_hdr})


def add_filter(request, kwargs, get_name, kwarg_name):
    courses = request.GET.getlist(get_name)

    for course in courses:
        if course != '':
            kwargs.append(course)


def schedule(request):
    if request.method == "POST":
        data = organize(request.POST)
        print(data)
        ret_data = sched(json.dumps(data))
        ret_dict = json.loads(ret_data)

        return render(
            request, 'schedule.html', {
                'scheduled': ret_dict['scheduled'],
                'unscheduled': ret_dict['unscheduled'],
                'header': site_hdr
            })

