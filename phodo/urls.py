#-*- coding: utf-8 -*-
from django.conf.urls import url
import views

app_name = 'phodo'

urlpatterns = [

    url(r'^r/$', views.RateView.as_view(), name='rate'), #index generate a rate and redirect to this page
    url(r'^r/(?P<pic_id>[0-9]+)/$', views.PicRateView.as_view(), name='picrate'), #for a rate for specific picture
    url(r'^login/$', views.login),
    url(r'^login/code(?P<wcde>\w+)/$', views.login),
    url(r'^upload/$', views.UploadView.as_view(), name='upload'),
    url(r'^result/$', views.ResultView.as_view(), name='result'),
    url(r'^$', views.IndexView.as_view(), name='index'),
]