from django.forms import ModelForm
from .models import Course


class FeedbackForm(forms.Form):

    fname = forms.CharField(label='First Name', required=True)
    lname = forms.CharField(label='Last Name', required=True)
    email_address = forms.EmailField(label='Email Address', required=True)
    comments = forms.CharField(label='Comments', required=True,
                               widget=forms.Textarea)


class CourseForm(ModelForm):
    isSelected = forms.BooleanField(label='', required=False)
