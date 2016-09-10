# forms center.
from django import forms

class LoginForm(forms.Form):
    user_name = forms.CharField(label='Your Name:', max_length=40)


