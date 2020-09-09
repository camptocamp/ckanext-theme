# /datanouvelleaquitaine/api/3/action/datastore_upsert

***Note : ** Il est aussi possible, dans certains cas, d'utiliser [datastore_create](datastore_create.md). Notamment
 si ce que l'on veut mettre à jour est le schéma des données.   
 Par contre, `datastore_create` n'acceptera pas d'insérer une 
 donnée existante,à supposer qu'une contrainte d'unicité (primary key) a été définie sur cette table.*

Cette commande permet d'ajouter des données, d'en remplacer, ou les deux. Elle nécessite qu'on ait déjà créé la table
, soit via l'UI, soit via l'API.

Par exemple, si l'on reprend l'exemple des aires de jeu donné dans [datastore_create](datastore_create.md), on pourra 
faire un upsert (update pour si l'id existe, insert sinon) : 

```
curl -k -d "@resource.json"  -H 'X-CKAN-API-Key:b31f9f2f-0f5b-40d4-b66d-038752f533a3'  https://dev2.pigma.org/datanouvelleaquitaine/api/3/action/datastore_upsert
```
où

**`resource.json`:**  
```json
{
    "resource_id": "5dba8454-5638-45de-af03-bd5ea1d178c9",
    "records": [
        {
            "id": 1,
            "nom": "Jardin des Dames de la Foi",
            "nature": "Aire de jeux",
            "nombre_jeux": 7,
            "age_min": 1.5,
            "age_max": 8,
            "num_quartier": 5
        },
        {
            "id": 4,
            "nom": "Parc Rivière",
            "nature": "Aire de jeux",
            "nombre_jeux": 5,
            "age_min": 1.5,
            "age_max": 10,
            "num_quartier": 2
        }
    ],
    "method": "upsert"
}
```

Si la donnée a été chargée via l'interface web, il faudra rajouter `"force": "True"`.