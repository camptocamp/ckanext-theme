# /datanouvelleaquitaine/api/3/action/datastore_search

La [documentation du datastore](https://docs.ckan.org/en/2.8/maintaining/datastore.html#ckanext.datastore.logic.action.datastore_search) est assez explicite. En complément, voilà quelques exemples : 
```
curl https://dev2.pigma.org/datanouvelleaquitaine/api/3/action/datastore_search?resource_id=5dba8454-5638-45de-af03-bd5ea1d178c9 |json_pp
```
On peut aussi ouvrir l'adresse directement dans le navigateur web : https://dev2.pigma.org/datanouvelleaquitaine/api/3/action/datastore_search?resource_id=5dba8454-5638-45de-af03-bd5ea1d178c9

Limiter le nombre de résultats : 
https://dev2.pigma.org/datanouvelleaquitaine/api/3/action/datastore_search?resource_id=5dba8454-5638-45de-af03-bd5ea1d178c9&limit=1

Choisir les champs récupérés : 
https://dev2.pigma.org/datanouvelleaquitaine/api/3/action/datastore_search?resource_id=5dba8454-5638-45de-af03-bd5ea1d178c9&fields=id,nom,nombre_jeux 

Filtrer les enregistrements : 
`https://dev2.pigma.org/datanouvelleaquitaine/api/3/action/datastore_search?resource_id=5dba8454-5638-45de-af03-bd5ea1d178c9&filters=%7B%22nombre_jeux%22:7%7D`

Attention : il est possible que l'URL ne passe pas dans le navigateur, car le filtre s'écrit {"nombre_jeux":7} or les accolades ne sont pas suportées dans une URL GET. Vous pouvez les encoder (%7B pour { et %7D pour }).
Ou bien faire une requête POST : 

```
curl -k -d '{"resource_id":"5dba8454-5638-45de-af03-bd5ea1d178c9", "filters":{"nombre_jeux":7}}'  -H 'X-CKAN-API-Key:b31f9f2f-0f5b-40d4-b66d-038752f533a3' https://dev2.pigma.org/datanouvelleaquitaine/api/3/action/datastore_search | json_pp
```

# /datanouvelleaquitaine/api/3/action/datastore_search_sql

Ce point d'accès API permet de faire des requêtes libres dans la base du datastore. C'est potentiellement très puissant.

Il semble qu'il y ait quelques difficultés à déclarer la requêtes SQL dans un objet json, avec curl. Mais il est possible de taper la requête directement dans l'URL du navigateur : 
`
https://dev2.pigma.org/datanouvelleaquitaine/api/3/action/datastore_search_sql?sql=SELECT * FROM "5dba8454-5638-45de-af03-bd5ea1d178c9" WHERE age_max > 9;
`
