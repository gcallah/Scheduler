from django import forms

class FeedbackForm(forms.Form):
    First_Name = forms.CharField(required=True)
    Last_Name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    Comments = forms.CharField(required=True, widget=forms.Textarea)

class ScheduleForm(forms.Form):
    First_Name = forms.CharField(required=True)
    Last_Name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    Comments = forms.CharField(required=True, widget=forms.Textarea)
