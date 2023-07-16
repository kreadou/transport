from django.conf.urls import url
from django.urls import re_path, path
from planning import views

app_name="planning"
urlpatterns = [
   url(r'accueil/$', views.accueil, name='accueil'),
   url(r'planning_creer/$', views.planning_creer, name='planning_creer'),
   url(r'planning_modifier/(?P<pk>[0-9]+)/$', views.planning_modifier, name='planning_modifier'),
   url(r'planning_visualiser/(?P<pk>[0-9]+)/$', views.planning_visualiser, name='planning_visualiser'),
   url(r'planning_delete/(?P<pk>[0-9]+)/$', views.planning_delete, name='planning_delete'),

]