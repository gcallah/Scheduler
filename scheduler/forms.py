from django import forms

def get_time_choices():
    choices_list = (
    ('1', '9:30AM - 10:45AM'),
    ('2', '11:00AM - 12:15PM'),
    ('3', '12:30PM - 1:45PM'),
    ('4', '02:00PM - 03:15PM'),
    ('5', '03:30PM - 04:45PM'),
    ('6', '05:00PM - 06:45PM'),
    ('7', '07:00PM - 8:15PM'),
    ('8', '08:30PM - 10:00PM'),
)
    return choices_list

class FeedbackForm(forms.Form):
    fname = forms.CharField(label='First Name', required=True)
    lname = forms.CharField(label='Last Name', required=True)
    email_address = forms.EmailField(label='Email Address', required=True)
    comments = forms.CharField(label='Comments', required=True, widget=forms.Textarea)

class ScheduleForm(forms.Form):
    fname = forms.CharField(label='First Name', required=True)
    lname = forms.CharField(label='Last Name', required=True)
    email_address = forms.EmailField(label='Email Address', required=True)    
    Course_being_taught = forms.CharField(required=True)
    time_slot = forms.TypedMultipleChoiceField(choices=get_time_choices,required=True)
