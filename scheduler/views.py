from django.shortcuts import render
from django.http import HttpResponse

site_hdr = "Course Scheduler"

def index(request):
    return render(request, 'index.html', {'header': site_hdr})

def about(request):
    return render(request, 'about.html', {'header': site_hdr})

def feedback(request):
    return render(request, 'feedback.html', {'header': site_hdr})

def requirements(request):
	return render(request, 'requirements.html', {'header': site_hdr})


