from django.conf.urls import url
from django.urls import re_path, path
from facturation import views

app_name="facturation"
urlpatterns = [
   url(r'accueil/$', views.accueil, name='accueil'),
   url(r'facturation_creer/$', views.facturation_creer, name='facturation_creer'),
   url(r'facturation_modifier/(?P<pk>[0-9]+)/$', views.facturation_modifier, name='facturation_modifier'),
   url(r'facturation_visualiser/(?P<pk>[0-9]+)/$', views.facturation_visualiser, name='facturation_visualiser'),
   url(r'facturation_delete/(?P<pk>[0-9]+)/$', views.facturation_delete, name='facturation_delete'),
   url(r'facturation_imprimer/(?P<pk>[0-9]+)/$', views.facturation_imprimer, name='facturation_imprimer'),
   url(r'facturation_imprimer_carburant/(?P<pk>[0-9]+)/$', views.facturation_imprimer_carburant, name='facturation_imprimer_carburant'),

   url(r'facturation_situation_ca/$', views.facturation_situation_ca, name='facturation_situation_ca'),
   url(r'facturation_situation_impaye/$', views.facturation_situation_impaye, name='facturation_situation_impaye'),

   url(r'facturation_lister_filtrer/$', views.facturation_lister_filtrer, name='facturation_lister_filtrer'),

   url(r'alerte_prise_carburant/$', views.alerte_prise_carburant, name='alerte_prise_carburant'),



]