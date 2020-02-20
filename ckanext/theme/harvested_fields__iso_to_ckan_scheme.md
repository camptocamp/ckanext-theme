# Correspondance entre champs ISO et champs CKAN 

*Il est conseillé de lire avant la [présentation du mécanisme de moissonnage](harvesting.md).*

La correspondance est en bonne partie établie dans la fonction [fix_harvest_scheme_fields](harvest_helpers.py).

La colonne CKAN reprend les champs définis dans [ckan_dataset.json](scheming/ckan_dataset.json)

| CKAN            | Description               | ISO (GeoNetwork) | Algo |
| :---            |    :----                  |:---              |:---              |
| title           | Nom de la donnée          | gmd:title        |     |
| name            | Nom de la donnée, sluggifié| gmd:title      | pas d'accent, espaces remplacés par _    |
| tag_string      | Mots clefs  | gmd:MD_Keywords/gmd:keyword      | [sanitize_keywords](harvest_helpers.py) : enlève les accents, espaces etc     |
| owner_org      | Organisation propriétaire (CKAN)  | -      |  |
| description      | Description / résumé  | gmd:abstract |  |
| thumbnail      | Aperçu (image)  | gmd:graphicOverview | lien (url) vers la ressource GN |
| themes      | Thématiques  | gmd:topicCategory + keywords INSPIRE| Valeurs matchent les thématiques/groupes ckan. Tableau de correspondance : [correspondance_iso_et_inspire_vers_ckan.xlsx](docs/correspondance_iso_et_inspire_vers_ckan.xlsx) |
| hyperlink      | TODO  | TODO| TODO|
| issued      | TODO  | TODO| TODO|
| modified      | TODO  | TODO| TODO|
| publisher      | TODO  | TODO| TODO|
| accrualPeriodicity      | TODO  | TODO| TODO|
| contactPoint      | TODO  | TODO| TODO|
| contactPoint_email      | TODO  | TODO| TODO|
| spatial-name      | TODO  | TODO| TODO|
| spatial-text      | TODO  | TODO| TODO|
| spatial      | TODO  | TODO| TODO|
| genealogy      | TODO  | TODO| TODO|
| resource_fields      | TODO  | TODO| TODO|

