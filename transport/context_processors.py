from datetime import datetime
from parametre.models import Alerte

def get_infos(request):
    date_actuelle = datetime.now()
    return {'date_actuelle': date_actuelle}


def alerte_synthese(request):

    type_alerte_vehicule = {}
    type_alerte_chauffeur = {}
    type_alerte_entretien = {}

    dataset = Alerte.alerte_view()
    #print ('alerte_list', dataset['alerte_list'])
    vehicule_list = dataset['vehicule_list']
    type_alerte_vehicule['assurance']=len(list(filter(lambda x: x.assurance <= dataset['alerte_list']['Assurance'], dataset['vehicule_list'])))
    
    type_alerte_vehicule['visite']=len(list(filter(lambda x: x.visite <= dataset['alerte_list']['Visite technique'], dataset['vehicule_list'])))
    type_alerte_vehicule['stationnement']=len(list(filter(lambda x: x.stationnement <= dataset['alerte_list']['Stationnement'], dataset['vehicule_list'])))
    type_alerte_vehicule['patente']=len(list(filter(lambda x: x.patente <= dataset['alerte_list']['Patente'], dataset['vehicule_list'])))
    total_alerte_vehicule = sum(type_alerte_vehicule.values())
    
    chauffeur_list = dataset['chauffeur_list']
    type_alerte_chauffeur['piece']=len(list(filter(lambda x: x.piece <= dataset['alerte_list']["Pièce d'identité"], dataset['chauffeur_list'])))
    type_alerte_chauffeur['permis']=len(list(filter(lambda x: x.permis <= dataset['alerte_list']['Permis de conduire'], dataset['chauffeur_list'])))
    type_alerte_chauffeur['acces']=len(list(filter(lambda x: x.acces <= dataset['alerte_list']['Carte accès portuaire'], dataset['chauffeur_list'])))
    total_alerte_chauffeur = sum(type_alerte_chauffeur.values())

    entretien_list = dataset['entretien_list']
    type_alerte_entretien['entretien']=len(list(filter(lambda x: x.prochain <= dataset['alerte_list']['Prochain entretien en date'], dataset['entretien_list'])))
    total_alerte_entretien = sum(type_alerte_entretien.values())

    return {'vehicule_list':vehicule_list, 
    'type_alerte_vehicule':type_alerte_vehicule,
    'total_alerte_vehicule':total_alerte_vehicule,

    'type_alerte_chauffeur':type_alerte_chauffeur,
    'total_alerte_chauffeur':total_alerte_chauffeur,

    'type_alerte_entretien':type_alerte_entretien,
    'total_alerte_entretien':total_alerte_entretien 
}


from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(is_safe=True)
def citation(texte):
    """
    Affiche le texte passé en paramètre, encadré de guillemets 
    français doubles et d'espaces insécables.
    """
    res = "«&nbsp;%s&nbsp;»" % escape(texte)
    return mark_safe(res)