from django.conf.urls import url
from django.urls import re_path, path
from ordretransport import views

app_name="ordretransport"
urlpatterns = [
   url(r'accueil/$', views.accueil, name='accueil'),
   url(r'ordretransport_creer/$', views.ordretransport_creer, name='ordretransport_creer'),
   url(r'ordretransport_modifier/(?P<pk>[0-9]+)/$', views.ordretransport_modifier, name='ordretransport_modifier'),
   url(r'ordretransport_visualiser/(?P<pk>[0-9]+)/$', views.ordretransport_visualiser, name='ordretransport_visualiser'),
   url(r'ordretransport_delete/(?P<pk>[0-9]+)/$', views.ordretransport_delete, name='ordretransport_delete'),

   url(r'ordretransport_imprimer/(?P<pk>[0-9]+)/$', views.ordretransport_imprimer,  name='ordretransport_imprimer'),

   url(r'ordretransport_lister_filtrer/$', views.ordretransport_lister_filtrer, name='ordretransport_lister_filtrer'),

]