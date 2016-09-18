from django.conf.urls import url
import views

app_name = 'phodo'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^r/$', views.RateView.as_view(), name='rate'), #index generate a rate and redirect to this page
    url(r'^r/(?P<pic_id>[0-9]+)/$', views.PicRateView.as_view(), name='picrate'), #for a rate for specific picture
]