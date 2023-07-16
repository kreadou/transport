from django.conf.urls import url
from django.urls import re_path, path
from client import views

app_name="client"

urlpatterns = [
   url(r'accueil/$', views.accueil, name='accueil'),
   url(r'client_creer/$', views.client_creer, name='client_creer'),
   url(r'client_modifier/(?P<pk>[0-9]+)/$', views.client_modifier, name='client_modifier'),
   url(r'client_visualiser/(?P<pk>[0-9]+)/$', views.client_visualiser, name='client_visualiser'),
   url(r'client_delete/(?P<pk>[0-9]+)/$', views.client_delete, name='client_delete'),

]