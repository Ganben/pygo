from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from django.views import View
from .models import Car, Picture
from .view.forms import LoginForm
from .view.forms import FileForm
# Create your views here.


class IndexView(ListView):
    model = Car

    def head(self, *args, **kwargs):
        car_list = self.get_queryset()._fetch_all()
        response = HttpResponse('')

        response['car_list'] = car_list
        return response

    def get(self, request, *args, **kwargs):
        render(request, 'profile.html')


class LoginView(View):
    form_class = LoginForm
    initial = {'key': 'value'}
    template_name = 'form_template.html'

    def get(self, request, *args, **kwargs):
        #write some query
        return render(request, 'login.html', {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form_class = LoginForm(request.POST)
        username = 'none'
        if form_class.is_valid():
            username = form_class.cleaned_data['user_name']

        #response.set_cookie('username', username)
        request.session['logged'] = True
        request.session['username'] = username
        return  render(request, 'result.html', {'username': username})

class PictureView(View):
    form_class = FileForm
    template_name = 'profile.html'
    saved = False
    def get(self, request, *args, **kwargs):
        return render(request, 'profile.html', {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = FileForm(request.POST, request.FILES)

        if form.is_valid():
            pic = Picture()
            pic.name = form.cleaned_data['name']
            pic.picture = form.cleaned_data['picture']
            pic.save()

            return render(request, 'saved.html', {'saved': True})
        else:
            return render(request, 'saved.html', {'saved': self.saved})
