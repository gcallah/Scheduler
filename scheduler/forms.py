from django import forms
from django.forms import ModelForm
from .models import *

class FeedbackForm(forms.Form):
    fname = forms.CharField(label='First Name', required=True)
    lname = forms.CharField(label='Last Name', required=True)
    email_address = forms.EmailField(label='Email Address', required=True)
    comments = forms.CharField(label='Comments', required=True, widget=forms.Textarea)

class ScheduleForm(ModelForm):

    cname = forms.ModelChoiceField(queryset=Course.objects.filter(), label='Course:', required=True)
    room = forms.ModelChoiceField(queryset=Room.objects.all(), label='Room:', required=True) 
    numStudents = forms.IntegerField(label='Number of Students:', required=True)

    class Meta:
        model = Schedule
        fields = ["cname", "room", "numStudents"]
