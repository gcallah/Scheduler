from django.shortcuts import render
from django.http import HttpResponse
from scheduler.forms import FeedbackForm
from scheduler.forms import ScheduleForm


site_hdr = "Course Scheduler"

def index(request):
    return render(request, 'index.html', {'header': site_hdr})

def about(request):
    return render(request, 'about.html', {'header': site_hdr})

def feedback(request):
    form_class = FeedbackForm
    return render(request, 'feedback.html', {'form': form_class,})

def requirements(request):
    return render(request, 'requirements.html', {'header': site_hdr})

def schedule(request):
    form_class = ScheduleForm
    return render(request, 'feedback.html', {'form': form_class,})

