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
    
    cname = forms.ModelMultipleChoiceField(queryset=TimeSlot.objects.filter(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Course
        fields = ["cname"]