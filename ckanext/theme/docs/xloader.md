# xloader : charger des données dans le datastore

Doc de référence xloader : https://github.com/ckan/ckanext-xloader

## Types de fichiers pris en charge
xloader ne prend en charge que les fichiers tabulaires :   

    'csv', 'application/csv',
    'xls', 'xlsx', 'tsv',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'ods', 'application/vnd.oasis.opendocument.spreadsheet'
    
 Les fichiers json et geojson ne sont pas nécessairement compatibles avec une structure tabulaire, et ne sont 
 apparemment pas supportés pour l'instant.
 De même, les shapefiles ne sont pas supportés.
 
 ## Champs géographiques
 
 Il y a cependant un niveau limité de support de données json et géographiques : il est possible de fournir un champ 
 json dans la donnée CSV.
Ce champ peut même inclure un objet geojson. Par exemple : 
```csv
Name,Position
"Paris","{""type"":""Point"",""coordinates"":[2.3508,48.8567]}"
```

## Mode de chargement
Les fichiers supportés sont chargés dans le datastore à la création de la ressource. Vous pouvez la recharger via 
l'onglet `Datastore`. Si le résultat du chargement ne s'affiche pas, rechargez la page.

### Changer le type des champs 
Par défaut, tous les champs sont considérés comme des champs texte. On peut changer ultérieurement le type des champs 
(numérique, date) : 
 * lorsque la donnée a été chargée une première fois, l'ouvrir en édition. 
 * Aller dans l'onglet `Dictionnaire de données`.
 * Changer le type (champ "Type prioritaire") pour les champs de donnée à modifier. Par exemple, changer les valeurs 
 numériques en type prioritaire 'numeric'
 * Enregistrer
 * Aller dans l'onglet `Datastore`
 * Cliquer sur 'Télécharger vers le datastore'
 * Pour voir le log du chargement, recharger la page.
 * Les modifications devraient être effectives. Pour le vérifier, vous pouvez tester le comportement dans la vue 
 tabulaire : une donnée numérique ou textuelle ne se triera pas de la même façon. Ou bien lancez une requête 
 [datastore_info](datastore/datastore_info.md)