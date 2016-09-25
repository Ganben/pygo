from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.views import View
from django.urls import reverse
from .models import Car, Picture, User
from .view.forms import LoginForm
from .view.forms import FileForm
import requests
import json

# Create your views here.
WECHAT_URL = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx1d3cfcf816c87d8b&redirect_uri=https%3A%2F%2Fwww.aishe.org.cn%2Fpark%2Flogin&response_type=code&scope=snsapi_base&state=123#wechat_redirect'

WECHAT_AUTHORIZE_URL = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=wx1d3cfcf816c87d8b&secret=e14e77b52e0c5ef7f496b8a88218c1eb&code='
#above is a id for http://mp.weixin.qq.com/debug/cgi-bin/sandboxinfo?action=showinfo&t=sandbox/index 'test account'

class IndexView(ListView):
    model = Car

    def head(self, *args, **kwargs):
        car_list = self.get_queryset()._fetch_all()
        response = HttpResponse('')

        response['car_list'] = car_list
        return response

    def get(self, request, *args, **kwargs):
        openid = request.session.get('openid', False)
        if not openid == False:
            u = User.objects.get(openid = openid)

        else:
            return HttpResponseRedirect(WECHAT_URL)  #redirect to wechat authorize page. see http://mp.weixin.qq.com/wiki/17/c0f37d5704f0b64713d5d2c37b468d75.html

        return render(request, 'profile.html')


class LoginView(View):
    form_class = LoginForm
    initial = {'key': 'value'}
    template_name = 'form_template.html'

    def get(self, request, *args, **kwargs):
        #write some query
        #if code not passed, return form; else direct login
        code = request.GET.get('CODE', 'X')   #path variable ?CODE=xxxxxxxx pass to code.
        if code == 'X':
            return render(request, 'login.html', {'form': self.form_class})
        else:
            res = requests.get(WECHAT_URL.join(code).join('&grant_type=authorization_code'))     # use wechat authorize api to fetch accesstoken, openid etc.
            data = json.loads(res)
            if data.get('errcode', 0) == 0:
                u = User(name=data.openid, openid=data.openid)
                u.save()
                request.session['login'] = True
                request.session['openid'] = data.openid


            else:
                return render(request, 'login.html', {'form': self.form_class})


    def post(self, request, *args, **kwargs):
        form_class = LoginForm(request.POST)
        username = 'none'
        if form_class.is_valid():
            username = form_class.cleaned_data['user_name']
            # user = User(name=username, openid=)
            #TODO connect with wechat authorize?
        #response.set_cookie('username', username)
        request.session['logged'] = True
        request.session['openid'] = username
        # return  render(request, 'result.html', {'username': username})
        return HttpResponseRedirect(reverse('phodo:upload'))

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
