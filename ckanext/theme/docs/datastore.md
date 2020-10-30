# Datastore

Espace de stockage en base de donnée qui permet de pousser des fichiers tabulaire (xls,csv). Cette fonctionnalité 
permet notamment de chercher, filtrer et mettre à jour les ressources sans avoir à télécharger ou uploader les fichiers.

## Via l'interface web
L'extension xloader permet de charger des données dans le datastore via l'interface web. Voir la doc 
[xloader](xloader.md)

## Télécharger la ressource complète
Le datastore offre une API permettant d'intéragir avec les données qui y ont été publiées.
Télécharger une ressource : 
* format CSV : `https://{CKAN-URL}/datastore/dump/{RESOURCE-ID}?bom=true`
* format json : `https://{CKAN-URL}/datastore/dump/{RESOURCE-ID}?format=json`
* format XML : `https://{CKAN-URL}/datastore/dump/{RESOURCE-ID}?format=xml`

## Chercher, filtrer les ressources
Voir [datastore_search](datastore/datastore_search.md)

## Mettre à jour les ressources
Voir [datastore_search](datastore/datastore_search.md)

## Utilisation de l'API datastore
* Recherche : [datastore_search et datastore_search_sql](datastore/datastore_search.md)
* Créer une nouvelle entrée : [datastore_create](datastore/datastore_create.md)
* Mettre à jour une entrée : [datastore_upsert](datastore/datastore_upsert.md) ou
 [datastore_create](datastore/datastore_create.md) (changer le schema de donnée)
* Supprimer une entrée dans le datastore : [datastore_delete](datastore/datastore_delete.md)
* Récupérer la structure de la donnée : [datastore_info](datastore/datastore_info.md)