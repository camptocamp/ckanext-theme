# Moissonnage de métadonnées
## Contexte
Le moissonnage des métadonnées est une action complexe. Particulièrement du fait de l'interaction de plusieurs extensions : 
* harvest est l'extension de base
* spatial ajoute la dimension géospatiale, avec un support ISO19139 en entrée, via CSW
* scheming définit la structure des metadonnées dans CKAN. Donc il interagit en imposant aux métadonnées moissonnées 
d'être conforme au schéma. Ce qui ne marche pas par défaut
* theme (cette extension) qui met son grain de sel, via le fichier harvest_helpers.py et en particulier la fonction 
`fix_harvest_scheme_fields`, pour assurer une compatibilité harvest/spatial/scheming. Elle intervient également sur les 
informations collectées et notamment alimente les chamsp définis via l'extension scheming.

## Moissonnage pas à pas
Le moissonnage passe donc par les étapes suivantes : 
1. harvest/spatial récupèrent la liste des enregistrements via des requêtes CSW getRecords
1. harvest/spatial récupèrent pour chaque enregistrement son contenu CSW, via une commande du type 
`https://www.geo2france.fr/geonetwork/srv/fre/csw-org-geo2france-opendata?OUTPUTFORMAT=application%2Fxml&SERVICE=CSW&OUTPUTSCHEMA=http%3A%2F%2Fwww.isotc211.org%2F2005%2Fgmd&REQUEST=GetRecordById&VERSION=2.0.2&ID=urn:isogeo:metadata:uuid:Lensd530bd7e-f1bb-e211-9ab3-00199985cd89&ElementSetName=full`
1. Le document XML est parsé par l'extension `spatial` notamment dans https://github.com/ckan/ckanext-spatial/blob/master/ckanext/spatial/model/harvested_metadata.py
et produit l'objet suivant [iso_values](docs/harvested_data/iso_values.md)
1. La métadonnée produite à l'issue de cet traitement est fourni dans l'objet [package_dict](docs/harvested_data/package_dict.md).
Cet objet ne contient pas, notamment, de valeurs pour les champs définis via l'extension scheming. Il n'est en fait pas compatible avec l'extension scheming, et en l'état, ne passera pa la validation : scheming attend que ses valeurs soient *à la racine de l'objet package_dict, et non dans les extras*
1. D'où l'importance de passer via la fonction `fix_harvest_scheme_fields`de cette extension : elle corrige la structure des données de sorte que 
le package passe la validation appliquée par l'extension scheming. Elle établit aussi une correspondance entre
des valeurs fournies dans iso_values et des champs du schema étendu de données défini via l'extension scheming.
L'objet sortant de cette fonction est le suivant : 
[package_dict après fix_harvest_scheme_fields](docs/harvested_data/packages_dict_after_fix_harvest_scheme_fields.md).
1. A l'issue du moissonnage, le package stocké dans CKAN peut être affiché via l'API pour voir sa structure : 
https://www.geo2france.fr/ckan/api/3/action/package_show?id=plan-de-vol-des-prises-de-vues-aeriennes-de-lorthophotographie-nord-pas-de-calais-2012-2013

Et pour simplifier les choses, si vous regardez dans la base de données, les champs définis par scheming sont stockés dans les extras.

## Correspondances des champs de métadonnées
Les champs CKAN et leur correspondance relative au métadonnées GeoNetwork sont détaillés dans [harvested_fields__iso_to_ckan_scheme.md](harvested_fields__iso_to_ckan_scheme.md).