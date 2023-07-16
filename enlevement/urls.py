from django.conf.urls import url
from django.urls import re_path, path
from enlevement import views

app_name="enlevement"
urlpatterns = [
   #url(r'accueil/$', views.accueil, name='accueil'),
   url(r'enlevement_lister/(?P<pk>[0-9]+)/$', views.enlevement_lister, name='enlevement_lister'),
   url(r'enlevement_creer/(?P<pk>[0-9]+)/$', views.enlevement_creer, name='enlevement_creer'),
   url(r'enlevement_modifier/(?P<pk>[0-9]+)/$', views.enlevement_modifier, name='enlevement_modifier'),
   url(r'enlevement_visualiser/(?P<pk>[0-9]+)/$', views.enlevement_visualiser, name='enlevement_visualiser'),
   url(r'enlevement_delete/(?P<pk>[0-9]+)/$', views.enlevement_delete, name='enlevement_delete'),

   url(r'enlevement_formset_creer/(?P<pk>[0-9]+)/$', views.enlevement_formset_creer, name='enlevement_formset_creer'),



]