# Correspondance entre champs ISO et champs CKAN 

*Il est conseillé de lire avant la [présentation du mécanisme de moissonnage](harvesting.md).*

La correspondance est en bonne partie établie dans la fonction [fix_harvest_scheme_fields](https://github.com/camptocamp/ckanext-theme/blob/19.12-geo2france/ckanext/theme/harvest_helpers.py#L414).

La colonne CKAN reprend les champs définis dans [ckan_dataset.json](scheming/ckan_dataset.json)

| CKAN            | Description               | ISO (GeoNetwork) | Algorithme |
| :---            |    :----                  |:---              |:---              |
| title           | Nom de la donnée          | gmd:title        |     |
| name            | Nom de la donnée, sluggifié| gmd:title      | pas d'accent, espaces remplacés par _    |
| tag_string      | Mots clefs  | gmd:MD_Keywords/gmd:keyword      | [sanitize_keywords](https://github.com/camptocamp/ckanext-theme/blob/19.12-geo2france/ckanext/theme/harvest_helpers.py#L530) : enlève les accents, espaces etc     |
| license_id      | License  | -      | Elle n'est pas récupérée. Valeur par défaut : 'other-at' |
| owner_org       | Organisation propriétaire (CKAN)  | -      | Organisation propriétaire du point de moissonnage |
| notes           | Description / résumé  | gmd:abstract |  |
| update_frequency| Fréquence de mise à jour de la donnée | gmd:MD_MaintenanceFrequencyCode @codeListValue| Convertit la valeur suivant le tableau de correspondances [update_frequencies](https://github.com/camptocamp/ckanext-theme/blob/19.12-geo2france/ckanext/theme/harvest_helpers.py#L13)|
| datatype        | Type de donnée  | - | Essaie de déterminer les valeurs valides parmi le choix (cf [ckan_dataset.json](https://github.com/camptocamp/ckanext-theme/blob/18.06-pigma/ckanext/theme/scheming/ckan_dataset.json#L48)). Fusionne le résultat avec les valeurs récupérées via le processus de moissonnage standard, permettant de définir des valeurs par défaut. Par exemple avec `{"default_extras": { "datatype": ["donnees-geographiques", "donnees-ouvertes"]}}` dans le champ de config du moissonnage |
| thumbnail       | Aperçu (image)  | gmd:graphicOverview | lien (url) vers la ressource GN |
| themes          | Thématiques  | gmd:topicCategory + keywords INSPIRE| Valeurs matchent les thématiques/groupes ckan. Tableau de correspondance : [correspondance_iso_et_inspire_vers_ckan.xlsx](docs/correspondance_iso_et_inspire_vers_ckan.xlsx) |
| category        | Catégorie, telle que définie dans  [ckan_dataset.json](https://github.com/camptocamp/ckanext-theme/blob/18.06-pigma/ckanext/theme/scheming/ckan_dataset.json#L94) |  |Non obtenu par moissonnage|
| hyperlink       | Lien web  | - | Non obtenu par moissonnage |
| inspire_url     | Lien vers la fiche GeoNetwork  |  - | [GeoNetwork-only] Concaténation harvester_url + champ guid. Sinon, retourne le champ unique-resource-identifier si dispo|
| granularity     | Granularité de la couverture territoriale  |  | Non obtenu par moissonnage |
| dataset_publication_date      | Date de publication  | gmd:CI_Date | gmd:CI_Date[gmd:dateType/ gmd:CI_DateTypeCode @codeListValue='publication']|
| dataset_modification_date      | Date de mise à jour de la donnée  | gmd:CI_Date | pseudo XPath : gmd:CI_Date[gmd:dateType/ gmd:CI_DateTypeCode @codeListValue='revision']|
| support         | Support technique  | - | Non obtenu par moissonnage |
| author      | Point de contact pour la métadonnée  | gmd:contact/gmd:CI_ResponsibleParty | Récupère le point de contact, avec un ordre de préférence sur le type de POC (défini en config `ckanext.theme.harvest.poc.priority.list = pointOfContact, author, owner, publisher, processor, originator, distributor, resourceProvider, custodian, principalInvestigator, user`). Affiche le nom de l'organisation si possible, sinon de l'individu|
| author_email      | Mail du point de contact  | gmd:contact/gmd:CI_ResponsibleParty/.. ../gmd:electronicMailAddress| Addresse mail, si dispo, du POC sélectionné ci-dessus|
| spatial-name      | Code de l'entité géographique  | - | Non obtenu par moissonnage |
| spatial-text      | Libellé de l'entité géographique  | - | Non obtenu par moissonnage |
| spatial      | Emprise géographique  | gmd:EX_GeographicBoundingBox | Traité par l'extension ckanext-spatial directement|
| resource_fields      | Ressources associées  | gmd:distributionInfo/.. ../gmd:CI_OnlineResource| |

