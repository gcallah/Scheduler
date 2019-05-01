from django.shortcuts import render
from scheduler.forms import FeedbackForm
from .schedalgo.schedule import sched
from .models import Course, Request
from .organize_data import organize, organize_output
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
        data_in = dict()
        if 'reschedule' in request.POST:
            for key in request.POST:
                if key == "csrfmiddlewaretoken":
                    data_in[key] = request.POST[key]
                else:
                    pos = key.find("_") 
                    if pos != -1:
                        course_name = key[:pos]
                        if course_name in data_in:
                            data_in[course_name] += 1
                        else:
                            data_in[course_name] = 1
        else:
            data_in = request.POST
        
        data = organize(data_in)
        ret_data = sched(json.dumps(data))
        ret_dict = json.loads(ret_data)

        scheduled = ret_dict['scheduled']
        unscheduled = ret_dict['unscheduled']

        ret_scheduled = organize_output(scheduled)

        new_request = Request()
        new_request.scheduled = str(ret_scheduled)
        new_request.unscheduled = str(unscheduled)
        new_request.save()

        return render(
            request, 'schedule.html', {
                'scheduled': ret_scheduled,
                'unscheduled': unscheduled,
                'header': site_hdr
            })
