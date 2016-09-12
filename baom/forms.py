#encoding=utf-8
from django import forms


class SubmitForm(forms.Form):
    name = forms.CharField(label='姓名', max_length=40)
    phone = forms.CharField(label='手机', max_length=30)
    number = forms.IntegerField(label='人数')
    is1 = forms.BooleanField(label='1号住>', required=False)
    is2 = forms.BooleanField(label='2号住>', required=False)
    is3 = forms.BooleanField(label='3号住>', required=False)