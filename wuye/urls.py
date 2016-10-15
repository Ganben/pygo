#-*- coding: utf-8 -*-
# ganben created

from django.conf.urls import url
import views

app_name = 'wuye'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
]