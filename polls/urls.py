from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    #ex: /polls/5
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    #ex: /polls/5/results/
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    #ex: /polls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),

    url(r'^posi/(?P<position_id>[0-9]+)/detail/$', views.parkdetail, name='park'),
    url(r'^parking/(?P<park_id>[0-9]+)/dopark/$', views.dopark, name='dopark'),
    url(r'^charging/(?P<park_id>[0-9]+)/endpark/$', views.endpark, name='endpark'),
    url(r'^charging/(?P<pos_id>[0-9]+)/parks/$', views.parks, name='parks'),
]
