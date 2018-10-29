from django.shortcuts import render
from django.http import HttpResponse
from scheduler.forms import FeedbackForm
from scheduler.forms import ScheduleForm
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template import loader
from .models import Schedule
from django import forms



site_hdr = "Course Scheduler"

def index(request):
    form = ScheduleForm()
    return render(request, 'index.html', {'form':form, 'header': site_hdr})

def about(request):
    return render(request, 'about.html', {'header': site_hdr})


#This feedback form old and will be redone using a model form, similar to the current def schedule function below.
def feedback(request):
    form_class = FeedbackForm
    
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            First_name = request.POST.get('First_name', '')
            Last_name = request.POST.get('Last_name', '')
            contact_email = request.POST.get('contact_email', '')
            comments = request.POST.get('Comments', '')

            template = get_template('feedback_template.txt')
            context = {
                'First_name': First_name,
                'Last_name': Last_name,
                'Contact_email': contact_email,
                'Comments': comments,
            }
            content = template.render(context)

            email = EmailMessage(
                "New contact form submission",
                content,
                "Your website" +'',
                ['youremail@gmail.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()

            return redirect('/scheduler/feedback')

    return render(request, 'feedback.html', {'form': form_class,})

def requirements(request):
    return render(request, 'requirements.html', {'header': site_hdr})

def schedule(request):

    if request.method=='POST':
        form = ScheduleForm(request.POST or None)
        
        if form.is_valid():
            form.save(commit=True)
    else:
        return render(request, "schedule.html")



