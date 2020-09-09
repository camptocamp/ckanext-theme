# Utiliser l'API CKAN
## publication de datasets
l'API CKAN propose l'action package_create, pour créer une nouvelle fiche dans le catalogue.
Cependant, Quelques éléments rendent l'action délicate à mettre en oeuvre, liés à l'intégration dans geOrchestra et à 
certaines spécificité du schema utilisé

### Authentification 
La manière recommandée pour s'authentifier est d'utiliser la clef API. Cependant, il faut la 
déclarer dans un header 
 'X-CKAN-API-Key' au lieu de 'Authorization', du fait de passer par le security-proxy geOrchestra.  
 Exemples : 
  
*Python* :  
`request.add_header('X-CKAN-API-Key', '68843c2b-dea5-4b2a-9dfb-200ff80e8499')`
 au lieu de  
 `request.add_header('Authorization', '68843c2b-dea5-4b2a-9dfb-200ff80e8499')`
 
*curl* :  
 utiliser l'option 
 `-H 'X-CKAN-API-Key:5d334494-3f01-4cc4-92e6-334c7d7b63ec' `
 
### Champs obligatoires
Le fichier [ckan_dataset.json](scheming/ckan_dataset_json) définit le schéma de métadonnées de 
cette instance CKAN. Tous les champs marqués comme `'required': true` doivent être présents dans la donnée json envoyée
via l'API

### Thématiques
Les thématiques sont un cas un peu particulier. Elles utilisent les _groupes CKAN_ de façon sous-jacente. 
Cependant, on ne les définira pas via le champ `groups`, qui renverrait une erreur _Forbidden_. On les définira via le 
champ `themes` défini dans  [ckan_dataset.json](scheming/ckan_dataset_json).

Un exemple fontionnel est fourni dans le fichier 
[create_package_example.py](scripts/snippets/api/create_package_example.py)

## Codelists
Dans l'interface web d'édition d'une métadonnée, cetaines valeurs sont proposées sous forme de listes. La plupart des 
listes sont fournies directement dans le fichier ckan_dataset.json. Pour celles qui ne le sont pas, vous pouvez  
obtenir ces listes via l'API :
 
### update_frequency
[CKAN_URL]/theme-api/update_frequency/list

### Etendue géographique
L'étendue géographique est obtenue par des recherches sur l'API data.gouv.fr (adresse configurée dans la variable de 
config `ckanext.theme.api.geoextent.name.autocomplete.url`). Elle est faite en deux étapes :

1. Récupérer l'identifiant (autocompletion)
par un appel au service  
`[CKAN_URL]/theme-api/geoextent/name/autocomplete?incomplete=[MA_CHAINE]`  
on obtient 
l'autocompletion de la chaine `MA_CHAINE`. Récupérer les valeurs de `name` et `id` pour l'entité retenue

2. Récupérer l'emprise géographique correspondante
par un appel au service  
`[CKAN_URL]/theme-api/geoextent/bbox?id=[ENTITY_ID]`  
on récupère l'emprise.

## Utiliser le datastore
Documentation officielle : 
 * datastore : https://docs.ckan.org/en/2.8/maintaining/datastore.html
 * xloader : https://github.com/ckan/ckanext-xloader
 
Nous proposons ici un complément de documentation : 
 * [datastore](docs/datastore/datastore.md)
 * [xloader](docs/xloader.md)