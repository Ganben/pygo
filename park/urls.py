from django.conf.urls import url

from . import views

app_name = 'park'

urlpatterns = [
    url(r'^$', views.index, name='index'),   #index is button to check, list to charge, free space to public
    url(r'^login/', views.login, name='login'),   #fake login page
    url(r'^check/', views.add, name='check'),  #check picture to get status, paid or new parking ticket
    url(r'^results/', views.end, name='results'),   #list of parking ticket, paid or not paid and end time, can be charge
    url(r'^user/', views.user, name='user'),    #user index page, a list of numbers
    url(r'^ticket/', views.ticket, name='ticket'),  #click car number to create a new ticket, and areas, can extend
]