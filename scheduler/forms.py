from django import forms


class FeedbackForm(forms.Form):

    fname = forms.CharField(label='First Name', required=True)
    lname = forms.CharField(label='Last Name', required=True)
    email_address = forms.EmailField(label='Email Address', required=True)
    comments = forms.CharField(label='Comments', required=True,
                               widget=forms.Textarea)


class CourseForm(forms.Form):
    isSelected = forms.BooleanField(label='', required=False)
