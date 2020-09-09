# /datanouvelleaquitaine/api/3/action/datastore_delete

Supprimer un entrée dans le datastore n'est pas le plus compliqué. Il suffit d'obtenir l'`id` de la ressource, soit via l'URL dans l'interface web, soit via l'action API package_show : 
```bash
curl https://dev2.pigma.org/datanouvelleaquitaine/api/3/action/package_show?id=xloader-test |json_pp
```
puis on lancer la commande
```
curl -k -d "{\"resource_id\":\"6d1e2608-ac2e-42bf-aaf6-8131bfa283ed\"}" -H 'X-CKAN-API-Key:b31f9f2f-0f5b-40d4-b66d-038752f533a3' https://dev2.pigma.org/datanouvelleaquitaine/api/3/action/datastore_delete
```
(mettre à jour clef API et resource_id)

Attention, ce n'est pas parce que la ressource est supprimée du datastore qu'elle est supprimée des ressources attachées au package. Une ressource est plus qu'une entrée dans le datastore, et une ressource n'en a même pas nécessairement une !
Il est donc possible qu'il y ait des effets de bord indésirables (vues non fonctionnelles par exemple)

Pour supprimer la ressource au complet, c'est `resource_delete` qu'on utilisera : 
 ```
curl -k -d '{"id":"6d1e2608-ac2e-42bf-aaf6-8131bfa283ed"}' -H 'X-CKAN-API-Key:b31f9f2f-0f5b-40d4-b66d-038752f533a3' https://dev2.pigma.org/datanouvelleaquitaine/api/3/action/resource_delete
```