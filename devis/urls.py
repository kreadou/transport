from django.conf.urls import url
from django.urls import re_path, path
from devis import views

app_name="devis"
urlpatterns = [
   url(r'accueil/$', views.accueil, name='accueil'),
   url(r'devis_creer/$', views.devis_creer, name='devis_creer'),
   url(r'devis_modifier/(?P<pk>[0-9]+)/$', views.devis_modifier, name='devis_modifier'),
   url(r'devis_visualiser/(?P<pk>[0-9]+)/$', views.devis_visualiser, name='devis_visualiser'),
   url(r'devis_delete/(?P<pk>[0-9]+)/$', views.devis_delete, name='devis_delete'),

   url(r'devis_detail_lister/(?P<pk>[0-9]+)/$', views.devis_detail_lister, name='devis_detail_lister'),
   
   url(r'devisdetail_creer/(?P<pk>[0-9]+)/$', views.devisdetail_creer, name='devisdetail_creer'),

   url(r'devisdetail_modifier/(?P<pk>[0-9]+)/$', views.devisdetail_modifier,  name='devisdetail_modifier'),

   url(r'devis_imprimer/(?P<pk>[0-9]+)/$', views.devis_imprimer,  name='devis_imprimer'),


	url(r'devis_transformer_facture/(?P<pk>[0-9]+)/$', views.devis_transformer_facture,  name='devis_transformer_facture'),


   
]