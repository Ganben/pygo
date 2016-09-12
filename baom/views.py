#encoding=utf-8

from django.shortcuts import render
from django import forms
from django.views import View
from .models import Item
from .forms import SubmitForm
# Create your views here.

class IndexView(View):
    initial = {'key': 'value'}
    template_name = 'index.html'
    # item_list = Item.objects.all()
    form_class = SubmitForm(initial={'number': 1})

    def get(self, request):
        item_list = Item.objects.all()
        return render(request, 'index.html', {'form': self.form_class, 'item_list': item_list})

    def post(self, request, *args, **kwargs):
        form=SubmitForm(request.POST)
        if form.is_valid():

            Item.objects.create(
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                is1 = form.cleaned_data['is1'],
                is2 = form.cleaned_data['is2'],
                is3 = form.cleaned_data['is3'],
                number=form.cleaned_data['number'],
            )

        item_list = Item.objects.all()

        return render(request, 'index.html', {'form': self.form_class, 'item_list': item_list})

