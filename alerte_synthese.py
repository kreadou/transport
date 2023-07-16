
from parametre.models import Alerte

def alerte_synthese():

    type_alerte_vehicule = {}
    type_alerte_chauffeur = {}
    type_alerte_entretien = {}

    dataset = Alerte.alerte_view()
    vehicule_list = dataset['vehicule_list']
    type_alerte_vehicule['assurance']=len(list(filter(lambda x: x.assurance <= 0, dataset['vehicule_list'])))
    type_alerte_vehicule['visite']=len(list(filter(lambda x: x.visite <= 0, dataset['vehicule_list'])))
    type_alerte_vehicule['stationnement']=len(list(filter(lambda x: x.stationnement <= 0, dataset['vehicule_list'])))
    type_alerte_vehicule['patente']=len(list(filter(lambda x: x.patente <= 0, dataset['vehicule_list'])))
    total_alerte_vehicule = sum(type_alerte_vehicule.values())
    
    chauffeur_list = dataset['chauffeur_list']
    type_alerte_chauffeur['piece']=len(list(filter(lambda x: x.piece <= 0, dataset['chauffeur_list'])))
    type_alerte_chauffeur['permis']=len(list(filter(lambda x: x.permis <= 0, dataset['chauffeur_list'])))
    type_alerte_chauffeur['acces']=len(list(filter(lambda x: x.acces <= 0, dataset['chauffeur_list'])))
    total_alerte_chauffeur = sum(type_alerte_chauffeur.values())

    entretien_list = dataset['entretien_list']
    type_alerte_entretien['entretien']=len(list(filter(lambda x: x.prochain <= 0, dataset['entretien_list'])))
    total_alerte_entretien = sum(type_alerte_entretien.values())

    return {'vehicule_list':vehicule_list, 
    'type_alerte_vehicule':type_alerte_vehicule,
    'total_alerte_chauffeur':total_alerte_vehicule,

    'type_alerte_chauffeur':type_alerte_chauffeur,
    'total_alerte_chauffeur':total_alerte_chauffeur,

    'type_alerte_entretien':type_alerte_entretien,
    'total_alerte_entretien':total_alerte_entretien 
    }
