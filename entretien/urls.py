from django.conf.urls import url
from django.urls import re_path, path
from entretien import views

app_name="entretien"
urlpatterns = [
   url(r'accueil/$', views.accueil, name='accueil'),
   url(r'entretien_creer/$', views.entretien_creer, name='entretien_creer'),
   url(r'entretien_modifier/(?P<pk>[0-9]+)/$', views.entretien_modifier, name='entretien_modifier'),
   url(r'entretien_visualiser/(?P<pk>[0-9]+)/$', views.entretien_visualiser, name='entretien_visualiser'),
   url(r'entretien_delete/(?P<pk>[0-9]+)/$', views.entretien_delete, name='entretien_delete'),

   url(r'fournisseur/add/$', views.CreateFournisseur.as_view(), name='add_fournisseur'),


]