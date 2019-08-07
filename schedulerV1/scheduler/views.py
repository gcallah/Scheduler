from django.shortcuts import render
from django.core.cache import cache
from django.utils import timezone
from scheduler.forms import FeedbackForm
from datetime import datetime, timedelta
from .schedalgo.schedule import sched
from .models import Course, Request
from .organize_data import organize, organize_output, organize_request
import json
import pickle
import os
import hashlib

site_hdr = "Course Scheduler"
max_sections = 5
history_data_path = "scheduler/history_schedule_data/"


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
        # Organize the input data into required format
        data_in = organize_request(request)
        data = organize(data_in)

        # Schedule the courses
        ret_data = sched(json.dumps(data))
        ret_dict = json.loads(ret_data)

        scheduled = ret_dict['scheduled']
        unscheduled = ret_dict['unscheduled']

        # Change the data into front-end required format
        ret_scheduled = organize_output(scheduled)

        # Store the historical data into db and local file system
        record_history(ret_scheduled, unscheduled)

        return render(
            request, 'schedule.html', {
                'scheduled': ret_scheduled,
                'unscheduled': unscheduled,
                'header': site_hdr
            })


def record_history(ret_scheduled, unscheduled):
    # Record the new schedule results
    new_request = Request()
    now = timezone.now()

    path = history_data_path + hashlib.sha256(repr(now).encode('utf-8')).hexdigest() + '.pkl'
    f = open(path, 'wb')
    pickle.dump((ret_scheduled, unscheduled), f)

    new_request.date_time = now
    new_request.path = path
    new_request.save()

    if int(now.day) % 7 == 0:
        # Remove the outdated records
        delta = timedelta(days=7)
        outdated = now - delta
        outdated_requests = Request.objects.filter(date_time__lte=outdated)
        for request in outdated_requests:
            if os.path.isfile(request.path):
                os.remove(request.path)
            request.delete()

        # Remove unrecorded files
        all_requests = Request.objects.all().order_by('-date_time')
        all_requests = list(map(lambda req: str(req.path), all_requests))
        file_list = os.listdir(history_data_path)
        for file_name in file_list:
            file_path = history_data_path+file_name
            if file_path not in all_requests:
                os.remove(history_data_path+file_name)


def request_history(request):
    all_requests = Request.objects.values_list('date_time', flat=True).order_by('-date_time')
    all_requests = list(filter(lambda x: x in all_requests, all_requests))

    return render(request, 'request_history.html', {
            'requests': all_requests,
            'header': site_hdr
        })


def resubmit(request):
    request_date = request.GET['req']
    res = cache.get(hash(request_date))
    if not res:
        record = Request.objects.get(date_time=request_date)
        f = open(record.path, 'rb')
        res = pickle.load(f)

        cache.set(hash(record.date_time), res)

    return render(request, 'schedule.html', {
            'scheduled': res[0],
            'unscheduled': res[1],
            'header': site_hdr
        })
