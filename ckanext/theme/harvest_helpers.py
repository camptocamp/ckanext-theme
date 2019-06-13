# coding: utf8
# CSW Harvest helper functions
import re
import urllib

from ckan.plugins.toolkit import config


# codelists used to get correspondence between geonetwork (iso_code) & etalab (eta_code), and also labels
update_frequencies = [
    {
        'iso_code': 'continual',
        'eta_code': 'continuous',
        'label_fr': 'Continue',
        'description_fr': ''
    },
    {
        'iso_code': 'daily',
        'eta_code': 'daily',
        'label_fr': 'Quotidienne',
        'description_fr': ''
    },
    {
        'iso_code': 'weekly',
        'eta_code': 'weekly',
        'label_fr': 'Hebdomadaire',
        'description_fr': ''
    },
    {
        'iso_code': 'fortnightly',
        'eta_code': 'biweekly',
        'label_fr': 'Bi-mensuelle',
        'description_fr': ''
    },
    {
        'iso_code': 'monthly',
        'eta_code': 'monthly',
        'label_fr': 'Mensuelle',
        'description_fr': ''
    },
    {
        'iso_code': 'quarterly',
        'eta_code': 'quarterly',
        'label_fr': 'Trimestrielle',
        'description_fr': ''
    },
    {
        'iso_code': 'biannually',
        'eta_code': 'semiannual',
        'label_fr': 'Semestrielle',
        'description_fr': ''
    },
    {
        'iso_code': 'annually',
        'eta_code': 'annual',
        'label_fr': 'Annuelle',
        'description_fr': ''
    },
    {
        'iso_code': 'asNeeded',
        'eta_code': 'irregular',
        'label_fr': 'Lorsque nécessaire',
        'description_fr': ''
    },
    {
        'iso_code': 'irregular',
        'eta_code': 'irregular',
        'label_fr': 'Sans régularité',
        'description_fr': ''
    },
    {
        'iso_code': 'notPlanned',
        'eta_code': 'punctual',
        'label_fr': 'Non plannifié',
        'description_fr': ''
    },
    {
        'iso_code': 'unknown',
        'eta_code': 'unknown',
        'label_fr': 'Inconnue',
        'description_fr': ''
    },
]


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