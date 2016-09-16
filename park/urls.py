from django.conf.urls import url
import views

# from django.views.generic import TemplateView    #TemplateView.as_view(template_name="about.html")

app_name = 'park'


urlpatterns = [
    # url(r'^$', views.Index.as_view(), name='index'),   #index is button to check, list to charge, free space to public
    url(r'^login/$', views.LoginView.as_view(), name='login'),   #fake login page
    # url(r'^check/', views.add, name='check'),  #check picture to get status, paid or new parking ticket
    # url(r'^results/', views.end, name='results'),   #list of parking ticket, paid or not paid and end time, can be charge
    # url(r'^user/', views.user, name='user'),    #user index page, a list of numbers
    # url(r'^ticket/', views.ticket, name='ticket'),  #click car number to create a new ticket, and areas, can extend
    url(r'^pic/$', views.PictureView.as_view(), name='pic'),
    url(r'^$', views.IndexView.as_view(), name='index'),
]