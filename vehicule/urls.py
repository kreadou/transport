from django.conf.urls import url
from django.urls import re_path, path
from vehicule import views

app_name="vehicule"
urlpatterns = [
   url(r'accueil/$', views.accueil, name='accueil'),
   url(r'vehicule_creer/$', views.vehicule_creer, name='vehicule_creer'),
   url(r'vehicule_modifier/(?P<pk>[0-9]+)/$', views.vehicule_modifier, name='vehicule_modifier'),
   url(r'vehicule_visualiser/(?P<pk>[0-9]+)/$', views.vehicule_visualiser, name='vehicule_visualiser'),
   url(r'vehicule_delete/(?P<pk>[0-9]+)/$', views.vehicule_delete, name='vehicule_delete'),

   url(r'imprimer_fiche/(?P<pk>[0-9]+)/$', views.imprimer_fiche, name='imprimer_fiche'),

]