from django import forms
from django.forms import ModelForm
from .models import *

class FeedbackForm(forms.Form):
    fname = forms.CharField(label='First Name', required=True)
    lname = forms.CharField(label='Last Name', required=True)
    email_address = forms.EmailField(label='Email Address', required=True)
    comments = forms.CharField(label='Comments', required=True,
                               widget=forms.Textarea)

class ScheduleForm(ModelForm):

    cname = forms.CharField(label='Course Name:', required=True)
   # room = forms.CharField(label='Room:', required=True)
    capacity = forms.IntegerField(label='Number of Students:', required=True)

    class Meta:
        model = Course
        fields = ["cname", "capacity"]
