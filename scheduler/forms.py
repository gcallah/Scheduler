from django import forms
from .models import *

class FeedbackForm(forms.Form):
    fname = forms.CharField(label='First Name', required=True)
    lname = forms.CharField(label='Last Name', required=True)
    email_address = forms.EmailField(label='Email Address', required=True)
    comments = forms.CharField(label='Comments', required=True, widget=forms.Textarea)

class ScheduleForm(forms.Form):
    pname = forms.ModelChoiceField(queryset=Professor.objects.values_list("pname", flat=True), label='Professor Name:', required=True) 
    cname = forms.ModelChoiceField(queryset=Course.objects.values_list("cname", flat=True), label='Course:', required=True) 
    room = forms.ModelChoiceField(queryset=Room.objects.values_list("rname", flat=True), label='Room:', required=True) 
    numStudents = forms.IntegerField(label='Number of Students:')


