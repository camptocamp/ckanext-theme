# Dataviz

## Fichiers geo

Pour la visu dans une carte, c'est l'extension [geoview](https://github.com/ckan/ckanext-geoview) qui est utilisée. Attention, cette extension n'est pas très active et sa doc n'est pas à 100% à jour.
Notamment : 
* le paramètre `feature_style` n'est actuellement pas fonctionnel (impossible de changer le style par défaut des features)

### GeoJSON

Pour qu'un fichier geojson soit affiché, le `format` de la donnée doit être défini en `geojson`.
 
 
### WMS
le `format` de la donnée doit être défini en `WMS`.

Pour qu'un flux WMS soit affiché, la syntaxe est un peu spécifique : 
* soit on veut fournir la liste des couches du flux, auquel cas on donnée l'URL vers le service WMS.

ex. :
* https://pigma.org/geoserver/urbanisme/wms listera toutes les couches du workspace urbanisme
* https://pigma.org/geoserver/urbanisme/wms#aquitaine_information_surf affichera uniquerment la couche aquitaine_information_surf  

### WFS
Pour l'instant, il semble bien que les flux WFS ne sont pas fonctionnels, malgré les affirmations de la doc.

### Couches à accès restreint
Pour les flux WMS et WFS, il faut aussi noter que seules les couches ouvertes, à accès libre, sont visualisables.