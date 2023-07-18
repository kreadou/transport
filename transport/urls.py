# -*- coding: utf-8 -*-
from django.contrib.auth import views as djviews
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^client/', include('client.urls')),
    url(r'^devis/', include('devis.urls')),
    url(r'^tableaubord/', include('tableaubord.urls')),
    url(r'^reglement/', include('reglement.urls')),
    url(r'^planning/', include('planning.urls')),    
    url(r'^reparation/', include('reparation.urls')),
    url(r'^entretien/', include('entretien.urls')),
    url(r'^alerte/', include('alerte.urls')),
    url(r'^facturation/', include('facturation.urls')),
    url(r'^enlevement/', include('enlevement.urls')),
    url(r'^ordretransport/', include('ordretransport.urls')),
    url(r'^marchandise/', include('marchandise.urls')),
    url(r'^commande/', include('commande.urls')),
    url(r'^detailscommande/', include('detailscommande.urls')),
    url(r'^carburant/', include('carburant.urls')),
    url(r'^vehicule/', include('vehicule.urls')),
    url(r'^chauffeur/', include('chauffeur.urls')),
    url(r'^$', djviews.LogoutView.as_view(next_page='parametre:login')), 
    url('ot', djviews.LogoutView.as_view(next_page='parametre:login')), 
    url('cocointer.pythonanywhere.net', djviews.LogoutView.as_view(next_page='parametre:login')), 
    url(r'^parametre/', include('parametre.urls')),
    url('admin/', admin.site.urls),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



"""

"""