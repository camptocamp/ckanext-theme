# /datanouvelleaquitaine/api/3/action/datastore_create

Créer une ressource dans le datastore avec le point d'entrée `datastore_create`:

`datastore_create` semble assez versatile, il n'est donc pas question de couvrir tous les cas de figure, mais au moins
les plus susceptibles d'être utilisés. Dans un premier temps, il est suggéré de lire la 
[doc du datastore](https://docs.ckan.org/en/2.8/maintaining/datastore.html#ckanext.datastore.logic.action.datastore_create).

Les exemples seront donnés avec la commande curl (ligne de commande). N'importe quelle autre méthode pour poster des 
données en mode POST devrait marcher de façon similaire.

## Terminologie

Rappel des terminologies CKAN : 
 * **package** : fiche de métadonnée
 * **ressource** : donnée associée à une fiche. Une ressource peut être un fichier, une URL, etc

## Commande curl

Dans tous les cas de figure, la commande à lancer sera 
```
curl -k -d "@resource.json"  -H 'X-CKAN-API-Key:b31f9f2f-0f5b-40d4-b66d-038752f533a3' https://dev2.pigma.org/datanouvelleaquitaine/api/3/action/datastore_create
```
Ajuster la clef d'API et si besoin l'URL (nom de domaine en particulier).  
***Ce qui différera, c'est le contenu du fichier resource.json***.

## Créer une ressource vide attachée à un package

Comme la doc le stipule, on peut créer une ressource vide attachée à un package donné. Cette ressource sera créée dans 
le datastore. Elle peut être totalement vide (même pas de définition du modèle de données).

### Pré-requis : identifiant du package

Il faut d'abord obtenir l'identifiant du package concerné. Souvent, on n'a que son nom. Le plus simple est d'utiliser l'action API `package_show`:

https://dev2.pigma.org/datanouvelleaquitaine/api/3/action/package_show?id=xloader-test

L'`id` sera dans la donnée renvoyée.

### Créer une ressource totalement vide

Pas le cas le plus probable, mais cette doc est incrémentielle (requête simple et petit d'abord, on complexifie au fur et à mesure).

**`resource.json`:**  
```json
{
  "resource": {
    "package_id":"9b415fbb-6d06-4901-87cc-deff9f0d47cd",
    "name":"my-empty-resource",
    "data_type":"file",
    "description": "RAS"
  }
}
```
 * `package_id` donne l'id récupéré via la requête `package_show`
 * `name`, `data_type` et `description` sont obligatoires, imposés par le schéma de la ressource (extension scheming, schema https://github.com/camptocamp/ckanext-theme/blob/pigma/ckanext/theme/scheming/ckan_dataset.json )

La réponse de la requête vous fournira entre autres l'`id` de la ressource ainsi créée.

### Créer une ressource vide de données

Le cas de figure précédent a peu de chance d'être souvent utile. A la rigueur comme emplacement temporaire à remplir plus tard. Plus vraisemblablement, vous voudrez au moins définir un schéma de donnée. Voici comment faire, avec le champ `fields`.

**`resource.json`:**  
```json
{
  "resource": {
    "package_id":"9b415fbb-6d06-4901-87cc-deff9f0d47cd",
    "name":"my-empty-resource2",
    "data_type":"file",
    "description": "RAS"
  },
  "fields":
        [
            {
              "id": "id",
              "type": "numeric", 
              "info": {"notes": "", "label": "id"}
            },
            {
              "id": "date",
              "type": "date", 
              "info": {"notes": "", "label": "date"}
            },
            {
              "id": "projet",
              "type": "text", 
              "info": {"notes": "", "label": "projet"}
            },
            {
              "id": "montant",
              "type": "numeric", 
              "info": {"notes": "", "label": "montant"}
            },
            {
              "id": "commentaires",
              "type": "text", 
              "info": {"notes": "", "label": "commentaires"}
            }
        ],
    "indexes": "projet",
    "primary_key": "id"
}
```
 * `package_id` donne l'id récupéré via la requête `package_show`
 * `name`, `data_type` et `description` sont obligatoires, imposés par le schéma de la ressource (extension scheming, schema https://github.com/camptocamp/ckanext-theme/blob/pigma/ckanext/theme/scheming/ckan_dataset.json )
 * `fields` fournit la structure des données (les colonnes dans la table postgresql). [Doc ckan](https://docs.ckan.org/en/2.8/maintaining/datastore.html#fields)
    * `id` est le nom du champ postgresql
    * `type` est le type de donnée. La liste est fournie dans la doc : https://docs.ckan.org/en/2.8/maintaining/datastore.html#fields. A noter que le dictionnaire de données (UI) ne reconnait apparemment que text, numeric et timestamp
    * le bloc `info` fournit un champ intéressant : `type_override` qui permet de surclasser une définition de type (*a posteriori*). Les deux autres champs sont informatifs mais n'apparaissent pas dans l'UI. `type_override` n'est pas utilisé à la création, on le verra plus bas.

La réponse de la requête vous fournira entre autres l'`id` de la ressource ainsi créée.

## Créer une ressource avec des données

Le plus probable est que vous ayez déjà des données à fournir au datastore. Auquel cas vous ajouterez un bloc [`records`](https://docs.ckan.org/en/2.8/maintaining/datastore.html#records) : 

**`resource.json`:**  
```json
{
  "resource":{
    "package_id":"9b415fbb-6d06-4901-87cc-deff9f0d47cd",
    "name":"aires de jeux (Bx)",
    "data_type":"file",
    "description": "Aires de jeu de Bordeaux (extrait). Source https://opendata.bordeaux-metropole.fr/explore/dataset/bor_airejeux/table/"
  },
  "fields":
        [
            {
              "id": "id",
              "type": "numeric", 
              "info": {"notes": "", "label": "id"}
            },
            {
              "id": "nom",
              "type": "text"
            },
            {
              "id": "nature",
              "type": "text", 
              "info": {"notes": "", "example": "Aire de jeux"}
            },
            {
              "id": "nombre_jeux",
              "type": "numeric"
            },
            {
              "id": "age_min",
              "type": "numeric"
            },
            {
              "id": "age_max",
              "type": "numeric"
            },
            {
              "id": "num_quartier",
              "type": "numeric"
            }
        ],

    "records": [
        {
            "id": 1,
            "nom": "Jardin des Dames de la Foi",
            "nature": "Aire de jeux",
            "nombre_jeux": 5,
            "age_min": 1.5,
            "age_max": 8,
            "num_quartier": 5
        },
        {
            "id": 2,
            "nom": "Place des Droits de l'Enfant",
            "nature": "Aire de jeux",
            "nombre_jeux": 11,
            "age_min": 1,
            "age_max": 12,
            "num_quartier": 7
        },
        {
            "id": 3,
            "nom": "Esplanade Charles de Gaulle",
            "nature": "Aire de jeux",
            "nombre_jeux": 7,
            "age_min": 1,
            "age_max": 12,
            "num_quartier": 3
        }
    ],
    "indexes": "nom, num_quartier,age_min,age_max",
    "primary_key": "id"
}
```
 * `primary_key` permet de définir une clef primaire sur la table (unicité des valeurs)
 * `indexes` des index postgresql   
 
En pratique, le datastore permet de définir un certain nombre d'objets postgresql : pkey, index, triggers, ainsi que de faire des recherches directement en SQL. Ces fonctions sont documentées dans la doc officielle du datastore : 
https://docs.ckan.org/en/2.8/maintaining/datastore.html#


## Mettre à jour une ressource

`datastore_create`, contrairement à ce que son nom indique, ne se limite pas à la création d'une ressource. Il permet aussi de mettre à jour le contenu et, surtout, le schema des données.

Pour une mise à jour, on utilisera l'`id` de la ressource, au lieu du `package_id`.

### Mettre à jour le schema
***Note** : Il semble que ça ne marche pas sur des données créées via l'API, mais ça marche sur des données créées via l'interface 
web (c'est ce que fait xloader quand il recharge les données dans le datastore, via le bouton "Télécharger dans le datastore")*

Supposons que vous ayez poussé une donnée avec un schema erroné (champs textuels alors qu'on a des valeurs numériques), par exemple.
Pour déclarer *a posteriori* les bons types de données, vous pouvez appliquer : 
```json
{
  "resource_id":"81b5ea01-3b0d-4d3a-9fd0-724f08c3fe00",
  "fields":
        [
            {
              "id": "id",
              "type": "numeric", 
              "info": {"notes": "", "label": "id"}
            },
            {
              "id": "nom",
              "type": "text"
            },
            {
              "id": "nature",
              "type": "text", 
              "info": {"notes": "", "example": "Aire de jeux"}
            },
            {
              "id": "nombre_jeux",
              "type": "text",
              "info": {"notes": "", "type_override": "numeric"}
            },
            {
              "id": "age_min",
              "type": "text",
              "info": {"notes": "", "type_override": "numeric"}
            },
            {
              "id": "age_max",
              "type": "text",
              "info": {"notes": "", "type_override": "numeric"}
            },
            {
              "id": "num_quartier",
              "type": "numeric"
            }
        ],
  "force": "True"
}
```

Si la donnée a été chargée via l'interface web, il faut rajouter `"force": "True"` (les données sont marquées comme 
'read-only').
