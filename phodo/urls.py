from django.conf.urls import url
import views

app_name = 'phodo'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<r_id>[0-9]+)/$', views.RateView.as_view(), name='rate'), #index generate a rate and redirect to this page
]