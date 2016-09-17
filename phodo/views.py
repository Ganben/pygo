from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import Rform
# Create your views here.

#here define the wechat api parameters.
#user and auth both use wechat pub xxx
WECHAT_URL = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx1d3cfcf816c87d8b&redirect_uri=https%3A%2F%2Fwww.aishe.org.cn%2Fpark%2Flogin&response_type=code&scope=snsapi_base&state=123#wechat_redirect'


class IndexView(View):
    #this view is to do 1, redirect to auth page(commom method)
    #let me see if django has some common tool; mixins or method decorator, not comprehensible
    # i just decide to use manually verify sessions. of course before i use salt sign, it will not be safe.
    def get(self, request, *args, **kwargs):
        openid = request.session.get('openid', None)
        if openid == None:
            return HttpResponseRedirect(WECHAT_URL)   #redirect to wechat authorize page. see http://mp.weixin.qq.com/wiki/17/c0f37d5704f0b64713d5d2c37b468d75.html
        else:
            #call a view to draw 2 picture to phodo
        #TODO a common method to randon 2 picture and to fill a rate form;
            r_id = 1 # auto generate r_id, = photo id , its rating times, pull another picture to compare with it.
            return HttpResponseRedirect(reverse('phodo:rate', args=(r_id,)))