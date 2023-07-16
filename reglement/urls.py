from django.conf.urls import url
from django.urls import re_path, path
from reglement import views

app_name="reglement"
urlpatterns = [
   url(r'accueil/$', views.accueil, name='accueil'),
   url(r'reglement_creer/$', views.reglement_creer, name='reglement_creer'),
   url(r'reglement_modifier/(?P<pk>[0-9]+)/$', views.reglement_modifier, name='reglement_modifier'),
   url(r'reglement_visualiser/(?P<pk>[0-9]+)/$', views.reglement_visualiser, name='reglement_visualiser'),
   url(r'reglement_delete/(?P<pk>[0-9]+)/$', views.reglement_delete, name='reglement_delete'),

]