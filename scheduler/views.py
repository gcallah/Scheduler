from django.shortcuts import render
from django.http import HttpResponse

site_hdr = "The DevOps Course"

def index(request):
    return render(request, 'index.html', {'header': site_hdr})


