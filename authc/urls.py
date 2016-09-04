from django.conf.urls import url

from . import views

app_name='authc'

urlpatterns = [
    url(r'^$', views.AccountViewSet, name='index'),
]