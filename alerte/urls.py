from django.conf.urls import url
from django.urls import re_path, path
from alerte import views

app_name="alerte"
urlpatterns = [
   url(r'accueil/$', views.accueil, name='accueil'),
   url(r'alerte_creer/$', views.alerte_creer, name='alerte_creer'),
   url(r'alerte_modifier/(?P<pk>[0-9]+)/$', views.alerte_modifier, name='alerte_modifier'),
   url(r'alerte_visualiser/(?P<pk>[0-9]+)/$', views.alerte_visualiser, name='alerte_visualiser'),
   url(r'alerte_delete/(?P<pk>[0-9]+)/$', views.alerte_delete, name='alerte_delete'),

   url(r'alerte_parametre/$', views.alerte_parametre, name='alerte_parametre'),

   url(r'alerte_parametre_creer/$', views.alerte_parametre_creer, name='alerte_parametre_creer'),
]