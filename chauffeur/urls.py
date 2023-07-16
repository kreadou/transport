from django.conf.urls import url
from django.urls import re_path, path
from chauffeur import views

app_name="chauffeur"
urlpatterns = [
   url(r'accueil/$', views.accueil, name='accueil'),
   url(r'chauffeur_creer/$', views.chauffeur_creer, name='chauffeur_creer'),
   url(r'chauffeur_modifier/(?P<pk>[0-9]+)/$', views.chauffeur_modifier, name='chauffeur_modifier'),
   url(r'chauffeur_visualiser/(?P<pk>[0-9]+)/$', views.chauffeur_visualiser, name='chauffeur_visualiser'),
   url(r'chauffeur_delete/(?P<pk>[0-9]+)/$', views.chauffeur_delete, name='chauffeur_delete'),

   url(r'imprimer_fiche/(?P<pk>[0-9]+)/$', views.imprimer_fiche, name='imprimer_fiche'),

]