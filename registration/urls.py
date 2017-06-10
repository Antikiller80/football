from django.conf.urls import url


from . import views

urlpatterns = [
    url(r'^login/$', views.LoginFormView.as_view(), name='login'),
    url(r'^register/$', views.RegisterFormView.as_view(), name='register_user'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.ProfileUpdate.as_view(), name='profileupdate'),
    url(r'^confirm/(?P<activation_key>\w+)/', views.register_confirm, name='register_confirm'),
    url(r'^profile/(?P<pk>[0-9]+)/$', views.ProfileView.as_view(), name='profileview'),
]
