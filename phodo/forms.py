#-*- coding: utf-8 -*-
#ganben 21.9.2016

from django.utils.encoding import python_2_unicode_compatible
from django import forms


# @python_2_unicode_compatible
class Rform(forms.Form):
     #this is a list of pictures and can be vote and sumitted; post
     #this form is a two elements form, so not plan loop
     #this form is going to rendered manually for style reason
     #this form is only for one radio choice field and post. the value should be the pic 1 win 2 and vise versal.
     def __init__(self, pics, *args, **kwargs):
          super(Rform, self).__init__(*args, **kwargs)
          self.fields['choice'] = forms.ChoiceField(
               choices=[(obj.id, obj.picture) for obj in pics],   #http://stackoverflow.com/questions/3429084/why-do-i-get-an-object-is-not-iterable-error
               widget=forms.RadioSelect
          )
     #hint: http://stackoverflow.com/questions/18382940/django-dynamic-choicefield-all-images-in-static-dir
     #radio buttion, choices init by passing var, and find the url of images, see above hints, the render page follows it too.
     #choice = forms.ChoiceField(label='Select a better one', widget=forms.RadioSelect)  #somw where to impl choice https://docs.djangoproject.com/el/1.10/ref/models/fields/#field-choices
     # choice = forms.ChoiceField()
     hidden_pic1 = forms.IntegerField(widget=forms.HiddenInput)
     hidden_pic2 = forms.IntegerField(widget=forms.HiddenInput)

class Rform2P(forms.Form):
     hidden_pic1 = forms.IntegerField(widget=forms.HiddenInput)
     hidden_pic2 = forms.IntegerField(widget=forms.HiddenInput)
     choice = forms.CharField()

# @python_2_unicode_compatible
class UploadForm(forms.Form):
     #TODO obviously here we need a dynamic choice selecting; to select the available photo topics = Tags.
     def __init__(self, tags, *args, **kwargs):
         super(UploadForm, self).__init__(*args, **kwargs)
         self.fields['choice'] = forms.ChoiceField(
              choices=[(obj.id, obj.name) for obj in tags],
              widget=forms.RadioSelect
         )
     # choice = forms.ChoiceField()
     text = forms.CharField(label='Text', max_length=60)
     picture = forms.FileField()
     o_id = forms.IntegerField(widget=forms.HiddenInput)
     # openid = forms.CharField(widget=forms.HiddenInput)

class UploadForm2P(forms.Form):
     text = forms.CharField(label='Text', max_length=60)
     picture = forms.FileField()
     choice = forms.CharField()