from django.conf.urls import url
from django.conf import settings
from . import views

urlpatterns = [
    url(r'^$', views.index_2, name='index_2'),
    url(r'^category/(?P<id>[0-9]+)/$', views.detail_category, name='detail'),
    url(r'^article/(?P<id>[0-9]+)/$', views.detail_article, name='detail_article'),
]
