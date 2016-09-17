#-*- coding: utf-8 -*-

from django import forms


class Rform(forms.Form):
     choice = forms.ChoiceField()  #somw where to impl choice https://docs.djangoproject.com/el/1.10/ref/models/fields/#field-choices