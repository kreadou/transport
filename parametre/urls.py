from django.contrib.auth import views as djviews
from django.conf.urls import url
from django.urls import re_path, path
from parametre.forms import LoginForm
from django.views.generic import TemplateView
from parametre import views

app_name="parametre"
urlpatterns = [
	url(r'accueil', views.accueil, name='accueil'),
	url(r'index', views.index, name='index'),
	url(r'operation', TemplateView.as_view(template_name='operation.html'), name='operation'),
	url(r'login/$', djviews.LoginView.as_view(template_name= 'login.html', authentication_form= LoginForm), name='login'),
    url(r'logout/$', djviews.LogoutView.as_view(next_page='parametre:login')), 

    url(r'depense/list/$', views.DepenseList.as_view(), name='depense_list'),
    url(r'depense/create/$', views.DepenseCreate.as_view(), name='depense_create'),
   	url(r'depense/<int:pk>/update/$', views.DepenseUpdate.as_view(), name='depense_update'),
    url(r'depense/<int:pk>/detail/$', views.DepenseDetail.as_view(), name='depense_detail'),
   	url(r'depense/<int:pk>/delete/$', views.DepenseDelete.as_view(), name='depense_delete'),

    url(r'marchandise/$', views.marchandise, name='marchandise'),
    url(r'trajet/$', views.trajet, name='trajet'),

     url(r'marque/$', views.marque, name='marque'),

    url(r'continent/$', views.continent, name='continent'),
    url(r'pays/$', views.pays, name='pays'),
    url(r'region/$', views.region, name='region'),
	url(r'departement/$', views.departement, name='departement'),
    url(r'ville/$', views.ville, name='ville'),
    url(r'commune/$', views.commune, name='commune'),
    url(r'societe/$', views.societe, name='societe'),

    url(r'alerte/$', views.alerte, name='alerte'),

    url(r'profil_lister/$', views.profil_lister, name='profil_lister'),
    url(r'profil_creer/$', views.profil_creer, name='profil_creer'),
    url(r'profil_modifier/(?P<pk>[0-9]+)/$', views.profil_modifier, name='profil_modifier'),

    url(r'fournisseur/$', views.fournisseur, name='fournisseur'),

    url(r'fonction/$', views.fonction, name='fonction'),
    url(r'profession/$', views.profession, name='profession'),


]

