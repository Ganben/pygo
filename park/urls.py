from django.conf.urls import url

from . import views

app_name = 'park'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.login, name='login'),
    url(r'^add/', views.add, name='add'),
    url(r'^end/', views.end, name='end'),

]