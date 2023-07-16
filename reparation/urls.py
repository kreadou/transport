from django.conf.urls import url
from django.urls import re_path, path
from reparation import views

app_name="reparation"
urlpatterns = [
   url(r'accueil/$', views.accueil, name='accueil'),
   url(r'reparation_creer/$', views.reparation_creer, name='reparation_creer'),
   url(r'reparation_modifier/(?P<pk>[0-9]+)/$', views.reparation_modifier, name='reparation_modifier'),
   url(r'reparation_visualiser/(?P<pk>[0-9]+)/$', views.reparation_visualiser, name='reparation_visualiser'),
   url(r'reparation_delete/(?P<pk>[0-9]+)/$', views.reparation_delete, name='reparation_delete'),

]