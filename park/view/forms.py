#-*- coding: utf-8 -*-
# forms center.
from django import forms

class LoginForm(forms.Form):
    user_name = forms.CharField(label='Your Name:', max_length=40)

class FileForm(forms.Form):
    name = forms.CharField(label='文件名', max_length=50)
    picture = forms.ImageField()
