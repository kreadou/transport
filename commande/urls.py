from django.conf.urls import url
from django.urls import re_path, path
from commande import views

app_name="commande"
urlpatterns = [
   url(r'accueil/$', views.accueil, name='accueil'),
   url(r'client/add/$', views.CreateClient.as_view(), name='add_client'),
   url(r'commande_creer/$', views.commande_creer, name='commande_creer'),
   url(r'commande_modifier/(?P<pk>[0-9]+)/$', views.commande_modifier, name='commande_modifier'),
   url(r'commande_visualiser/(?P<pk>[0-9]+)/$', views.commande_visualiser, name='commande_visualiser'),
   url(r'commande_delete/(?P<pk>[0-9]+)/$', views.commande_delete, name='commande_delete'),

   url(r'marchandise/add/$', views.CreateMarchandise.as_view(), name='add_marchandise'),
   url(r'trajet/add/$', views.CreateTrajet.as_view(), name='add_trajet'),


   url(r'commande_imprimer/(?P<pk>[0-9]+)/$', views.commande_imprimer, name='commande_imprimer'),

   url(r'commande_filtrer/$', views.commande_filtrer, name='commande_filtrer'),

]

