from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^player/(?P<pk>[0-9]+)/$', views.PlayerDetailView.as_view(), name='playerview'),
    url(r'^club/(?P<pk>[0-9]+)/$', views.ClubDetailView.as_view(), name='clubview'),
    url(r'^match/(?P<pk>[0-9]+)/$', views.MatchesDetailView.as_view(), name='matchesview'),
    url(r'^championship/(?P<pk>[0-9]+)/$', views.ChampionshipDetailView.as_view(), name='championshipview'),
    url(r'^tour/(?P<tour>[0-9]+)/$', views.matchtourdetail, name='matchtourdetail'),
]
