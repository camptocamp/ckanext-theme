# coding: utf8
# CSW Harvest helper functions
from collections import OrderedDict
import json
import re
import urllib

from ckan.plugins.toolkit import config
from ckan.lib.munge import substitute_ascii_equivalents


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
        'label_fr': u'Non planifié',
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
    "amenagement": {
        'label_fr': u'Aménagement',
        'iso_themes': (
            u'structure',
        ),
        'inspire_themes': (
            u"Occupation des terres",
            u"Usage des sols",
        ),
    },
    "donnees-reference": {
        'label_fr': u'Données de référence',
        'iso_themes': (
            u'boundaries',
            u'elevation',
            u'imageryBaseMapsEarthCover'
            u'location',
            u'planningCadastre',
        ),
        'inspire_themes': (
            u"Dénominations géographiques",
            u"Ortho-imagerie",
            u"Parcelles cadastrales",
            u"Référentiels de coordonnées",
            u"Régions maritimes",
            u"Répartition de la population — démographie",
            u"Systèmes de maillage géographique",
            u"Unités administratives",
            u"Unités statistiques",
        ),
    },
    "economie-emploi": {
        'label_fr': u'Économie et emploi',
        'iso_themes': (
            u'economy',
            u'farming',
        ),
        'inspire_themes': (
            u"Installations agricoles et aquacoles",
            u"Lieux de production et sites industriels",
        ),
    },
    "education-formation": {
        'label_fr': u'Education et formation',
        'iso_themes': (),
        'inspire_themes': (
        ),
    },
    "environnement-risques-sante": {
        'label_fr': u'Environnement, risques et santé',
        'iso_themes': (
            u'biota',
            u'climatologyMeteorologyAtmosphere',
            u'environment'
            u'geoscientificInformation',
            u'health',
            u'inlandWaters',
            u'intelligenceMilitary',
            u'oceans',
        ),
        'inspire_themes': (
            u"Caractéristiques géographiques océanographiques",
            u"Conditions atmosphériques",
            u"Géologie",
            u"Habitats et biotopes",
            u"Hydrographie",
            u"Installations de suivi environnemental",
            u"Régions biogéographiques",
            u"Répartition des espèces",
            u"Ressources minérales",
            u"Santé et sécurité des personnes",
            u"Sites protégés",
            u"Sols",
            u"Zones à risque naturel",
            u"Zones de gestion, de restriction ou de réglementation et unités de déclaration",
        ),
    },
    "institutions-partenariats": {
        'label_fr': u'Institutions et partenariats',
        'iso_themes': (
            u'utilitiesCommunication',
        ),
        'inspire_themes': (
            u"Services d'utilité publique et services publics",
        ),
    },
    "reseaux-energies": {
        'label_fr': u'Réseaux et énergies',
        'iso_themes': (),
        'inspire_themes': (
            u"Sources d'énergie",
        ),
    },
    "transports-mobilites": {
        'label_fr': u'Transports et mobilités',
        'iso_themes': (
            u'transportation',
        ),
        'inspire_themes': (
            u"Réseaux de transport",
        ),
    },
    "culture": {
        'label_fr': u'Vie sociale et culturelle',
        'iso_themes': (
            u'society',
        ),
        'inspire_themes': (
        ),
    },
})

# used to define the format from the resource protocol. The first entry is the beginning of the protocol name,
# the second is the format name
protocol_format_correspondance = {
    ('OGC:WMS', 'WMS'),
    ('OGC:WMTS', 'WMTS'),
    ('OGC:WFS', 'WFS'),
    ('OGC:GML', 'GML'),
    ('OGC:KML', 'KML'),
}


def _get_sub(extras_dict, key, sub_key_k, sub_value_k, id, default=''):
    sub = _get_value(extras_dict, key)
    try:
        d = json.loads(sub)
        return next(item[sub_value_k] for item in d if id in item[sub_key_k])
    except:
        return default


def _get_value(extras_dict, key, default_value=''):
    """
    Get the value out of a dict structured like the extras_keys_dict (see below) if the key exists. Return default_value
    if the key is absent or not properly structured
    :param extras_dict:
    :param key:
    :return:
    """
    try:
        return extras_dict.get(key)['value']
    except:
        return default_value


def _gn_csw_build_inspire_link(harvester_source, iso_values):
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


def _get_poc(iso_values, poc_priority_list):
    """
    CKAN harvest tend to mix point of contact information if several are provided.
    This function scans the point of contacts and returns the first one. Priority order is given by the
    poc_priority_list var
    :param iso_values: harvested values
    :param poc_priority_list: list of comma-separated poc types, e.g. "pointOfContact, author, owner, publisher, processor, originator, distributor, resourceProvider, custodian, principalInvestigator, user"
    :return: point of contact object
    """
    pocs = iso_values.get('metadata-point-of-contact')
    # pocs = [{'contact-info': {'online-resource': '', 'email': ''}, 'role': 'pointOfContact', 'organisation-name': u"Communaut\xe9 d'Agglom\xe9ration de Saint-Quentin", 'individual-name': '', 'position-name': ''}, {'contact-info': {'online-resource': '', 'email': 'info@aerodata-france.com'}, 'role': 'author', 'organisation-name': 'Aerodata France', 'individual-name': '', 'position-name': ''}]
    if not pocs:
        return None
    pocs_ordered = sorted(pocs, key=lambda x: poc_priority_list.index(x.get('role')))
    return pocs_ordered[0]


def _get_themes(iso_values, combine_themes=True):
    """
    Extract themes
     * if there is [1..n] ISO themes, it is mapped to a pigma theme
     * else, if there is [1..n] inspire theme keywords, we try the mapping with them
    Themes are managed as ckan groups
    :param iso_values:
    :return: list of {'id': theme} unique objects
    """
    #TODO: optimize search (create reverse-mapping dicts, cached so we don't recreate them on the fly for every dataset)
    groups = []
    iso_themes = iso_values.get('topic-category')
    for th in iso_themes:
        # try to find it in the pigma themes map
        for group_id, group_def in themes.items():
            if th in group_def['iso_themes']:
                groups.append({'id': group_id})
    if combine_themes or len(groups)==0:
        # if iso themes don't work, try with inspire themes
        for group_id, group_def in themes.items():
            for keyword in iso_values.get('keyword-inspire-theme'):
                if keyword in group_def['inspire_themes']:
                    groups.append({'id': group_id})

    # deduplicate our list. We can't use a set because dicts are not hashable
    groups = {v['id']:v for v in groups}.values()
    return groups


def _update_frequency_iso_to_eta(freq):
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
        # default is last entry
        freq = update_frequencies[-1]['eta_code']
    return freq


def _infer_datatypes(extras_dict):
    dt = []
    # Look for open source licence hints
    # TODO: if possible, be exhaustive...
    lic = _get_value(extras_dict, 'access_constraints', None)
    if lic:
        lic_values = json.loads(lic)
        # see if lists intersect
        if list(set(open_licence_tags) & set(lic_values)):
            dt.append(u'donnees-ouvertes')

    # check resource type
    # TODO: identify the values for u'donnees-intelligentes' and u'rapports-etudes'
    type = _get_value(extras_dict, 'resource-type', None)
    if type == 'dataset':
        dt.append(u'donnees-geographiques')

    return dt if dt else [u'donnees-geographiques'] # we need to provide at least one value


def _guess_resource_datatype(resource, default='other'):
    """
    Try to guess a data_type value in conformity with the choices given in the ckan scheme
    :param resource: the resource object to use
    :param default: default value if nothing relevant is found
    :return:
    """
    # TODO: improve the guessing work
    if resource['resource_locator_protocol'] in ['WWW:LINK-1.0-http--link']:
        if resource['format'] is None:
            return 'api'
        else:
            return 'doc'
    if resource['resource_locator_protocol'] in ['WWW:DOWNLOAD-1.0-http--download']:
        if resource['format'] in ['doc', 'docx', 'pdf']:
            return 'doc'
        else:
            return 'file'
    return default


def _guess_resource_format(resource):
    for f in protocol_format_correspondance:
        if resource['resource_locator_protocol'].startswith(f[0]):
            return f[1]
    if resource['url'].endswith('geojson'):
        return 'application/geojson'
    return ''


def _fix_resource(resource):
    """
    Resources attached to a metadata might have some fields not set that might make ckan complain like 'data_type'
    This fixes the missing fields, trying to fill them with relevant information when possible.
    The fixes are applied in-place in the resource object
    :param resource:
    :return:
    """
    if 'format' not in resource or not resource['format']:
        resource['format'] = _guess_resource_format(resource)
    if 'data_type' not in resource or resource['data_type'] == '':
        resource['data_type'] = _guess_resource_datatype(resource)
    if 'description' not in resource or resource['description'] == '':
        resource['description'] = u'Non renseigné'


def fix_harvest_scheme_fields(package_dict, data_dict):
    """
    Harvest does not work well with custom scheme defined using ckanext-scheming extension: if some harvested fields,
    stored in package['extras'], are named similar to a field in the scheming schema (ckan_dataset.json), there is a
    validation error. Scheming does not look for these values in extras (must be at root), but does not accept similar
    keys in extras as it would cause trouble during data storage.
    Solution is to get those values from extras, put them at package root so scheming can use them and remove those
    values from extras. This is what this function does. The modifications are done in-situ in the package_dict
    Also computes values from geonetwork metadata
    Beware: fields that are not in the custom schema still have to be stored in the extras. If not, they won't be stored
    in the database, hence lost after the harvest

    We also add tags transformation (make them loosely compliant) by default. To deactivate this behaviour, set
    {'compliant_tags':false} in the harvesting configuration (true by default)
    :param package_dict: original package_dict
    :return:
    """
    # custom fields need to go to top level:
    # package_dict['extras']['my_field'] becomes package_dict['my_field']
    # FIXME read fields from ckanext-scheming
    # FIXME handle different source and target schemas
    #        e.g. through field mapping in harvest config?
    # FIXME customise fields to your ckanext-scheming dataset schema
    fields = ['title', 'name', 'tag_string',
              'owner_org', 'description', 'accrualPeriodicity',
              'thumbnail', 'hyperlink',
              'issued', 'modified', 'publisher', 'contactPoint', 'contactPoint_email',
              'spatial', 'spatial-name', 'spatial-text', 'genealogy']
    # make extras a dictionary, so we can more easily access the records
    extras_keys_dict = {d['key']: d for d in package_dict['extras']}
    iso_values = data_dict['iso_values']

    for field in fields:
        if field in extras_keys_dict.keys():
            package_dict[field] = extras_keys_dict[field]['value']
            extras_keys_dict.pop(field, None)

    # Sanitize the tags
    # we need to retrieve the harvest configuration and check
    # * that `clean_tags` is unset or False (if not, we let the harvest extension run the clean_tags task (munge_tag(tag))
    #   see https://docs.ckan.org/projects/ckanext-spatial/en/latest/harvesters.html#overview-and-configuration
    #   and https://github.com/ckan/ckanext-harvest
    # * that our custom config option, `compliant_tags` is not explicitly set to False
    harvest_config = dict()
    try:
        harvest_config = json.loads(data_dict['harvest_object'].source.config, '{}')
    except:
        pass
    if harvest_config.get('compliant_tags', True) and not harvest_config.get('clean_tags', False):
        for tag in package_dict['tags']:
            tag['name'] = sanitizeKeyword(tag['name'], strict=False)

    try:
        # try to get the GN uuid as id for the dataset
        package_dict['id'] = iso_values['guid']
    except:
        pass
    package_dict['description'] = package_dict['notes']
    package_dict['thumbnail'] = _get_value(extras_keys_dict, 'graphic-preview-file', '')
    frequency = _get_value(extras_keys_dict, 'frequency-of-update', 'unknown')
    package_dict['accrualPeriodicity'] = _update_frequency_iso_to_eta(frequency)
    for resource in package_dict['resources']:
        _fix_resource(resource)

    # Compute values not present as-is in geonetwork
    package_dict['hyperlink'] = _gn_csw_build_inspire_link(data_dict['harvest_object'].source, iso_values)
    package_dict['topic-categories'] = ', '.join(iso_values.get('topic-category'))
    # set a consistent point of contact (name & email match a same entity instead of random-ish)
    poc_priority_list = config.get('ckanext.theme.harvest.poc.priority.list')
    poc = _get_poc(iso_values, poc_priority_list)
    if poc:
        # get organisation name if available, else individual name
        package_dict['contactPoint'] = poc.get('organisation-name', poc.get('individual-name', ''))
        package_dict['contactPoint_email'] = poc.get('contact-info').get('email', '')
    # get publisher poc, and if not available, fall-back to global poc
    try:
        publisher_poc = _get_poc(iso_values, "publisher")
        package_dict['publisher'] = poc.get('organisation-name', poc.get('individual-name', ''))
    except:
        package_dict['publisher'] = package_dict.get('contactPoint','')

    package_dict['modified'] = _get_sub(extras_keys_dict, 'dataset-reference-date', 'type', 'value', 'revision') or _get_sub(extras_keys_dict, 'dataset-reference-date', 'type', 'value', 'creation')
    package_dict['issued'] = _get_sub(extras_keys_dict, 'dataset-reference-date', 'type', 'value', 'publication')
    package_dict['genealogy'] = iso_values.get('lineage','')
    # Support datatype default_values from harvest config
    # ex.: `{"default_extras": { "datatype": ["donnees-geographiques", "donnees-ouvertes"]}}` in the configuration field
    # of the harvest
    datatypes = json.loads(package_dict.get('datatype', '[]'))
    # merge lists with unique values
    package_dict['datatype'] = list(set(datatypes + _infer_datatypes(extras_keys_dict)))
    package_dict['groups'] = _get_themes(iso_values)
    # We now use the `themes` schema field to manage the themes, then synced to groups. So we need to set the themes
    # values:
    package_dict['themes'] = [gp['id'] for gp in package_dict['groups']]

    # add some extra fields. Those fields, as they are not in the schema, have to be stored in extras
    extras_keys_dict['data-format'] = {'key': 'data-format', 'value': ', '.join(f['name'] for f in iso_values.get('data-format'))}
    #extras_keys_dict['maintainer_email'] = {'key': 'maintainer_email', 'value': _get_value(extras_keys_dict, 'contact-email', '')}
    extras_keys_dict['metadata_created'] = {'key': 'metadata_created', 'value': _get_value(extras_keys_dict, 'metadata-date', '')}
    extras_keys_dict['metadata_modified'] = {'key': 'metadata_modified', 'value': _get_value(extras_keys_dict, 'metadata-date', '')}

    # Finally, drop extras as scheming doesn't allow extras FALSE ! No need, just remove the scheming synonyms from extras
    # extras_keys_dict.pop('extras', None)
    package_dict['extras'] = extras_keys_dict.values()

def sanitizeKeyword(s, strict=True):
    """
    Make string compatible for usage as CKAN keywords:
    keywords rules are not very clear. It seems at first it did not support anything out of lowercased characters and _-
    but is seems that now it supports well spaces and uppercased chars, as well as accentuated characters.
    or -_

    This is an alternative to setting {"clean_tags": true} in the harvesting configuration,which is a little bit more destructive
    (although maybe quite similar to the strict option)
    :param s:
    :return:
    """

    if not s:
        return ''

    s = re.sub(r'\'\s+', ' ',   s) # remove duplicate spaces
    s = s.strip() # remove trailing spaces
    s = re.sub(u'\'', ' ', s) # Change single quote to space
    #s = re.sub(r'[\s]', '_', s)
    if strict:
        # should ensure compiancy with ckan validators requirements (as announced)
        #s = unidecode.unidecode(s)  # remove accents and keep to closest possible ascii match
        s = substitute_ascii_equivalents(s)  # remove accents and keep to closest possible ascii match
        pattern = u'[^\w\-]' # set a more strict match pattern
        s = re.sub(pattern, '-', s, re.UNICODE).lower() # all lowercased
    else:
        # seems sufficient in most cases
        pattern = u'[^a-zA-Z0-9_àâäôéèëêïîçùûüÿæœÀÂÄÔÉÈËÊÏÎŸÇÙÛÜÆŒ \-]' # Accept accents
        s = re.sub(pattern, '-', s, re.UNICODE) # don't lowercase systematically
    return s
