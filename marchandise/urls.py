from django.conf.urls import url
from django.urls import re_path, path
from marchandise import views

app_name="marchandise"
urlpatterns = [
   url(r'accueil/$', views.accueil, name='accueil'),
   url(r'trajet/add/$', views.CreateTrajet.as_view(), name='trajet_add'),
   url(r'marchandise/add/$', views.CreateMarchandise.as_view(), name='marchandise_add'),
   url(r'marchandise_creer/$', views.marchandise_creer, name='marchandise_creer'),
   url(r'marchandise_modifier/(?P<pk>[0-9]+)/$', views.marchandise_modifier, name='marchandise_modifier'),
   url(r'marchandise_visualiser/(?P<pk>[0-9]+)/$', views.marchandise_visualiser, name='marchandise_visualiser'),
   url(r'marchandise_delete/(?P<pk>[0-9]+)/$', views.marchandise_delete, name='marchandise_delete'),
   
   url(r'source/add/$', views.CreateSource.as_view(), name='source_add'),
   url(r'destination/add/$', views.CreateDestination.as_view(), name='destination_add'),
   url(r'vehicule/add/$', views.CreateVehicule.as_view(), name='vehicule_add'),
   url(r'chauffeur/add/$', views.CreateChauffeur.as_view(), name='chauffeur_add'),

   url(r'commune/add/$', views.CreateCommune.as_view(), name='commune_add'),

   url(r'commune/(?P<pk>[0-9]+)/$', views.commune, name='commune'),
]