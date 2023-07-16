from django.conf.urls import url
from django.urls import re_path, path
from detailscommande import views

app_name="detailscommande"
urlpatterns = [
   #url(r'accueil/$', views.accueil, name='accueil'),
   url(r'detailscommande_lister/(?P<pk>[0-9]+)/$', views.detailscommande_lister, name='detailscommande_lister'),
   url(r'detailscommande_creer/(?P<pk>[0-9]+)/$', views.detailscommande_creer, name='detailscommande_creer'),
   url(r'detailscommande_modifier/(?P<pk>[0-9]+)/$', views.detailscommande_modifier, name='detailscommande_modifier'),
   url(r'detailscommande_visualiser/(?P<pk>[0-9]+)/$', views.detailscommande_visualiser, name='detailscommande_visualiser'),
   url(r'detailscommande_delete/(?P<pk>[0-9]+)/$', views.detailscommande_delete, name='detailscommande_delete'),

]