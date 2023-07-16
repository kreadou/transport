from django.conf.urls import url
from django.urls import re_path, path
from tableaubord import views

app_name="tableaubord"
urlpatterns = [
   url(r'accueil/$', views.accueil, name='accueil'),
   url(r'accueil_filtrer/$', views.accueil_filtrer, name='accueil_filtrer'),
   url(r'vehicule_tableaubord/$', views.vehicule_tableaubord, name='vehicule_tableaubord'),
   url(r'chauffeur_tableaubord/$', views.chauffeur_tableaubord, name='chauffeur_tableaubord'),
   url(r'entretien_tableaubord/$', views.entretien_tableaubord, name='entretien_tableaubord'),

   url(r'carburant_tableaubord/$', views.carburant_tableaubord, name='carburant_tableaubord'),
   url(r'reparation_tableaubord/$', views.reparation_tableaubord, name='reparation_tableaubord'),
  
   url(r'enlevement/$', views.enlevement, name='enlevement'),
   url(r'enlevement_traitement/$', views.enlevement_traitement, name='enlevement_traitement'),

   url(r'statistique/$', views.statistique, name='statistique'),
   url(r'statistique_filtrer/$', views.statistique_filtrer, name='statistique_filtrer'),

]
