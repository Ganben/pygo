from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from django.views import View
from .models import Car
from .views.forms import LoginForm
# Create your views here.

class IndexView(ListView):
    model = Car

    def head(self, *args, **kwargs):
        car_list = self.get_queryset()._fetch_all()
        response = HttpResponse('')

        response['car_list'] = car_list
        return response


class LoginView(View):
    form_class = LoginForm
    initial = {'key': 'value'}
    template_name = 'form_template.html'

    def get(self, request, *args, **kwargs):
        #write some query
        return render(request, 'login.html', {'form': self.form_class})

    def post(self, request, *args, **kwargs):

        return render(request, 'result')

