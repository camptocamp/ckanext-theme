# coding: utf8
# CSW Harvest helper functions
from collections import OrderedDict
import json
import re
import urllib

from ckan.plugins.toolkit import config


# codelists used to get correspondence between geonetwork (iso_code) & etalab (eta_code), and also labels
update_frequencies = [
    {
        'iso_code': u'continual',
        'eta_code': u'continuous',
        'label_fr': u'Continue',
        'description_fr': u''
    },
    {
        'iso_code': u'daily',
        'eta_code': u'daily',
        'label_fr': u'Quotidienne',
        'description_fr': u''
    },
    {
        'iso_code': u'weekly',
        'eta_code': u'weekly',
        'label_fr': u'Hebdomadaire',
        'description_fr': u''
    },
    {
        'iso_code': u'fortnightly',
        'eta_code': u'biweekly',
        'label_fr': u'Bi-mensuelle',
        'description_fr': u''
    },
    {
        'iso_code': u'monthly',
        'eta_code': u'monthly',
        'label_fr': u'Mensuelle',
        'description_fr': u''
    },
    {
        'iso_code': u'quarterly',
        'eta_code': u'quarterly',
        'label_fr': u'Trimestrielle',
        'description_fr': u''
    },
    {
        'iso_code': u'biannually',
        'eta_code': u'semiannual',
        'label_fr': u'Semestrielle',
        'description_fr': u''
    },
    {
        'iso_code': u'annually',
        'eta_code': u'annual',
        'label_fr': u'Annuelle',
        'description_fr': u''
    },
    {
        'iso_code': u'asNeeded',
        'eta_code': u'irregular',
        'label_fr': u'Lorsque nécessaire',
        'description_fr': u''
    },
    {
        'iso_code': u'irregular',
        'eta_code': u'irregular',
        'label_fr': u'Sans régularité',
        'description_fr': u''
    },
    {
        'iso_code': u'notPlanned',
        'eta_code': u'punctual',
        'label_fr': u'Non plannifié',
        'description_fr': u''
    },
    {
        'iso_code': u'unknown',
        'eta_code': u'unknown',
        'label_fr': u'Inconnue',
        'description_fr': u''
    },
]

open_licence_tags = [
    "Aucune raison de restriction",
    "Licence Ouverte",
]

# dict used to define the CKAN categories list (edit form). also used during harvesting to scan the ISO or INSPIRE
# categories and transform them to categories in this list.
# TODO: update the groups.csv file and deduplicate this config. Maybe all in a csv file
themes = OrderedDict({
    "administration": {
        'label_fr': u'Administration et action publique',
        'iso_themes': (
            u'utilitiesCommunication'
        ),
        'inspire_themes': (
            u"Services d'utilité publique et services publics"
        ),
    },
    "agriculture": {
        'label_fr': u'Agriculture, sylviculture et viticulture',
        'iso_themes': (u'farming'),
        'inspire_themes': (
            u"Installations agricoles et aquacoles"
        ),
    },
    "amenagement": {
        'label_fr': u'Aménagement et urbanisme',
        'iso_themes': (),
        'inspire_themes': (
            u"Adresses",
            u"Zones de gestion, de restriction ou de réglementation et unités de déclaration"
        ),
    },
    "citoyennete": {
        'label_fr': u'Citoyenneté et démocratie',
        'iso_themes': (),
        'inspire_themes': (),
    },
    "culture": {
        'label_fr': u'Culture, patrimoine et tourisme',
        'iso_themes': (),
        'inspire_themes': (),
    },
    "economie": {
        'label_fr': u'Economie et entreprises',
        'iso_themes': (u'economy'),
        'inspire_themes': (
            u"Lieux de production et sites industriels"
        ),
    },
    "energie": {
        'label_fr': u'Energies et réseaux',
        'iso_themes': (),
        'inspire_themes': (
            u"Sources d'énergie"
        ),
    },
    "environnement": {
        'label_fr': u'Energies et réseaux',
        'iso_themes': (
            u'environment',
            u'climatologyMeteorologyAtmosphere',
            u'biota'
            u'geoscientificInformation',
            u'inlandWaters',
            u'elevation'
        ),
        'inspire_themes': (
            u"Régions biogéographiques",
            u"Habitats et biotopes",
            u"Répartition des espèces",
            u"Conditions atmosphériques",
            u"Caractéristiques géographiques météorologiques",
            u"Sites protégés",
            u"Sols",
            u"Géologie",
            u"Ressources minérales",
            u"Zones à risque naturel",
            u"Altitude",
            u"Hydrographie"
        ),
    },
    "equipement": {
        'label_fr': u'Equipements, bâtiments et logement',
        'iso_themes': (
            u'structure',
            u'intelligenceMilitary'
        ),
        'inspire_themes': (
            u"Bâtiments",
            u"Installations de suivi environnemental"
        ),
    },
    "formation": {
        'label_fr': u'Formation, éducation et emploi',
        'iso_themes': (),
        'inspire_themes': (),
    },
    "mer": {
        'label_fr': u'Mer et littoral',
        'iso_themes': (
            u'oceans'
        ),
        'inspire_themes': (
            u"Régions maritimes",
            u"Caractéristiques géographiques océanographiques"
        ),
    },
    "imagerie": {
        'label_fr': u'Imagerie et occupation du sol',
        'iso_themes': (
            u'imageryBaseMapsEarthCover',
            u'planningCadastre'
        ),
        'inspire_themes': (
            u"Ortho-imagerie",
            u"Occupation des terres",
            u"Parcelles cadastrales",
            u"Usage des sols"
        ),
    },
    "limites-administratives": {
        'label_fr': u'Limites administratives et référentiels',
        'iso_themes': (
            u'boundaries'
        ),
        'inspire_themes': (
            u"Unités administratives",
            u"Unités statistiques",
            u"Dénominations géographiques"
        ),
    },
    "mobilite": {
        'label_fr': u'Mobilité et transports',
        'iso_themes': (
            u'transportation'
        ),
        'inspire_themes': (
            u"Réseaux de transport"
        ),
    },
    "sciences": {
        'label_fr': u'Sciences, recherche et innovation',
        'iso_themes': (),
        'inspire_themes': (),
    },
    "sante": {
        'label_fr': u'Social, santé et sports',
        'iso_themes': (
            u'health',
            u'society'
        ),
        'inspire_themes': (
            u"Santé et sécurité des personnes",
            u"Répartition de la population-Démographie"
        )
    }
})

def get(pkg, key, default=''):
    val = filter(lambda x: x['key'] == key, pkg.get('extras', []))
    val = val[0]['value'] if len(val) > 0 else ''
    return val or default


def get_sub(pkg, key, sub_key_k, sub_value_k, id, default=''):
    sub = get(pkg, key)
    try:
        d = json.loads(sub)
        return next(item[sub_value_k] for item in d if id in item[sub_key_k])
    except:
        return default

def gn_csw_build_inspire_link(harvester_source, iso_values):
    """
    Try to produce a geonetwork permalink out of harvester url and metadata uuid
    :param harvester_source:
    :param iso_values:
    :return:
    """
    url = ''
    if harvester_source.type == u'csw':
        harvester_url = harvester_source.url
        # Try several strategies:
        # 1. Try to compute the URL by contenation of the source's base url and the metadata's UUID
        #    extract base URL (should be fine at least with geonetwork catalogs):
        base_url = re.search('(.*)/csw[\w-]*', harvester_url)
        if base_url.group(1):
            url = u"{}/catalog.search#/metadata/{}".format(base_url.group(1), iso_values.get('guid'))
        #TODO: check if the url is valid and if not try other ways, like for instance the unique-resource-identifier value
        # or try other patterns matching catalogs other than geonetwork
        if urllib.urlopen(url).getcode() == 200:
            return url

        # 2. Return the value of unique-resource-identifier if valid
        url = iso_values.get('unique-resource-identifier')
        if urllib.urlopen(url).getcode() == 200:
            return url

    # else...
    return ''


def get_poc(iso_values):
    """
    CKAN harvest tend to mix point of contact information if several are provided.
    This function scans the point of contacts and returns the first one. Priority order is given by the
    poc_priority_list var
    :param iso_values: harvested values
    :return: point of contact object
    """
    poc_priority_list = config.get('ckanext.theme.harvest.poc.priority.list')
    pocs = iso_values.get('metadata-point-of-contact')
    # pocs = [{'contact-info': {'online-resource': '', 'email': ''}, 'role': 'pointOfContact', 'organisation-name': u"Communaut\xe9 d'Agglom\xe9ration de Saint-Quentin", 'individual-name': '', 'position-name': ''}, {'contact-info': {'online-resource': '', 'email': 'info@aerodata-france.com'}, 'role': 'author', 'organisation-name': 'Aerodata France', 'individual-name': '', 'position-name': ''}]
    if not pocs:
        return None
    pocs_ordered = sorted(pocs, key=lambda x: poc_priority_list.index(x.get('role')))
    return pocs_ordered[0]


def get_themes(iso_values):
    """
    Extract themes
     * if there is [1..n] ISO themes, it is mapped to a pigma theme
     * else, if there is [1..n] inspire theme keywords, we try the mapping with them
    Themes are managed as ckan groups
    :param iso_values:
    :return:
    """
    #TODO: optimize search (create reverse-mapping dicts, cached so we don't recreate them on the fly for every dataset)
    groups = []
    iso_themes = iso_values.get('topic-category')
    for th in iso_themes:
        # try to find it in the pigma themes map
        for group_id, group_def in themes.items():
            if th in group_def['iso_themes']:
                groups.append({'id': group_id})
    if len(groups)==0:
        # if iso themes don't work, try with inspire themes
        for group_id, group_def in themes.items():
            for keyword in iso_values.get('keyword-inspire-theme'):
                if keyword in group_def['inspire_themes']:
                    groups.append({'id': group_id})
    return list(groups)


def update_or_set_extra(package_dict, key, value):
    """
    If the key already exists, replace its value. Else append this key/value pair
    :param package_dict: the dict to update
    :param key:
    :param value:
    :return:
    """
    # get the first entry in the list comprehension
    entry = next((x for x in package_dict['extras'] if x['key'] == key), None)
    if entry:
        entry['value'] = value
    else:
        package_dict['extras'].append({'key': key, 'value': value})


def update_frequency_iso_to_eta(freq):
    """
    return the eta_code (etalab value) for the given iso_code
    :param freq:
    :return:
    """
    matches = (x['eta_code'] for x in update_frequencies if freq == x['iso_code'] )
    # return the first occurrence matching the criteria
    try:
        freq = next(matches)
    except:
        freq = update_frequencies[-1]['eta_code']
    return freq


def infer_datatypes(pkg):
    dt = []
    # Look for open source licence hints
    # TODO: if possible, be exhaustive...
    lic = get(pkg, 'access_constraints')
    if lic:
        lic_values = json.loads(lic)
        # see if lists intersect
        if list(set(open_licence_tags) & set(lic_values)):
            dt.append(u'donnees-ouvertes')

    # check resource type
    # TODO: identify the values for u'donnees-intelligentes' and u'rapports-etudes'
    type = get(pkg, 'resource-type')
    if type == 'dataset':
        dt.append(u'donnees-geographiques')

    return dt if dt else [u'donnees-geographiques'] # we need to provide at least one value


def fix_harvest_scheme_fields(package_dict):
    """
    Harvest does not work well with custom scheme defined using ckanext-scheming extension: if some harvested fields,
    stored in package['extras'], are named similar to a field in the scheming schema (ckan_dataset.json), there is a
    validation error. Scheming does not look for these values in extras (must be at root), but does not accept similar
    keys in extras as it would cause trouble during data storage.
    Solution is to get those values from extras, put them at package root so scheming can use them and remove those
    values from extras. This is what this function does. The modifications are done in-situ in the package_dict
    :param package_dict: original package_dict
    :return:
    """
    # custom fields need to go to top level:
    # package_dict['extras']['my_field'] becomes package_dict['my_field']
    # FIXME read fields from ckanext-scheming
    # FIXME handle different source and target schemas
    #        e.g. through field mapping in harvest config?
    # FIXME customise fields to your ckanext-scheming dataset schema
    fields = ['title', 'name', 'tag_string', 'license_id',
              'owner_org', 'notes', 'update_frequency',
              'datatype', 'thumbnail', 'category', 'hyperlink', 'inspire_url',
              'dataset_publication_date', 'dataset_modification_date', 'support', 'author', 'author_email',
              'spatial', 'spatial-name', 'spatial-text']
    # make extras a dictionary, so we can more easily access the records
    extras_keys = {d['key']: d for d in package_dict['extras']}
    for field in fields:
        if field in extras_keys.keys():
            package_dict[field] = extras_keys[field]['value']
            extras_keys.pop(field, None)

    package_dict['license_id'] = u'notspecified'
    package_dict['datatype'] = u'unknown'
    # TODO: deal with situation where this is not defined
    package_dict['thumbnail'] = extras_keys['graphic-preview-file']['value']
    # TODO: complete with fields from schema
    # TODO: clean code
    frequency = 'unknown'
    try:
        frequency = extras_keys.get('frequency-of-update')['value']
    except:
        # If we get an error, then default value will be the one defined above
        pass
    package_dict['update_frequency'] = update_frequency_iso_to_eta(frequency)
    # package_dict['resources'] = [
    #     {
    #         'resource_locator_function': '',
    #         'name': 'Service WMS et WFS',
    #         'format': 'ZIP',
    #         'url': 'https://data.bordeaux-metropole.fr/key',
    #         'resource_locator_protocol': 'WWW:LINK-1.0-http--link',
    #         'description': u"Service WMS et WFS de Bordeaux M\xe9tropole (demander votre cl\xe9 d'acc\xe8s)",
    #         'data_type':'file'
    #     }
    # ]
    for res in package_dict['resources']:
        if res.get('data_type', None) is None:
            # TODO: infer proper data_type depending on protocol / format
            res['data_type'] = 'file'

    # append remainder of package_dict to package notes
    # for field in package_dict['extras'].keys():
    #     package_dict['notes'] += "\n###{0}\n{1}".format(field.title(), str(package_dict['extras'][field]))

    # Finally, drop extras as scheming doesn't allow extras FALSE ! No need, just remove the scheming synonyms from extras
    # extras_keys.pop('extras', None)
    package_dict['extras'] = extras_keys.values()

    return package_dict