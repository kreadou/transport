from django.conf.urls import url
from django.urls import re_path, path
from carburant import views

app_name="carburant"
urlpatterns = [
   url(r'accueil/$', views.accueil, name='accueil'),
   url(r'carburant_creer/$', views.carburant_creer, name='carburant_creer'),
   url(r'carburant_modifier/(?P<pk>[0-9]+)/$', views.carburant_modifier, name='carburant_modifier'),
   url(r'carburant_visualiser/(?P<pk>[0-9]+)/$', views.carburant_visualiser, name='carburant_visualiser'),
   url(r'carburant_delete/(?P<pk>[0-9]+)/$', views.carburant_delete, name='carburant_delete'),

]