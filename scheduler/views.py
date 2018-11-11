from django.shortcuts import render
from django.http import HttpResponse
from scheduler.forms import FeedbackForm
from scheduler.forms import CourseForm
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template import loader
from .models import Course
from .models import Room
from django import forms

site_hdr = "Course Scheduler"

def index(request):
    form = CourseForm
    course_list = Course.objects.all().order_by('cname')

    context = {'course_list':course_list,
                'form':form,
                'header':site_hdr,
    }

    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html', {'header': site_hdr})


#This feedback form old and will be redone using a model form, similar to the current def schedule function.
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

def addCourse(request):
    if request.method=='POST':
        
        #form = ScheduleForm(request.POST or None)
        
        if form.is_valid():
            form.save(commit=True)
            return render(request, "index.html", {'form': form})
        else:
            return HttpResponse(400)

def schedule(request):

    all_courses = Course.objects.all().order_by('-capacity')
    all_rooms = Room.objects.all().order_by('-capacity')

    scheduled_rooms = {}
    for course in all_courses:
        for room in all_rooms:
            if room.rname not in scheduled_rooms and course.cname not in scheduled_rooms.values():
                if course.capacity < room.capacity:
                    scheduled_rooms[room.rname] = course.cname

    #print(scheduled_rooms)
    return render(request, 'schedule.html', {'dictionary': scheduled_rooms}) 