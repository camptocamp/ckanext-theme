# Template helper functions
from ckan.lib.helpers import dict_list_reduce

from harvest_helpers import update_frequencies, themes

def dict_list_or_dict_reduce(list_, key, unique=True):
    """
    Hack to make helpers.dict_list_reduce work also if provided a dict of dicts instead of a list of dicts
    """
    if isinstance(list_, dict):
        list_ = list_.values()
    res = dict_list_reduce(list_, key, unique)
    return res


def list_data_formats(package):
    """
    Improved list of available formats.
    By default, CSW haravester has a poor file format guessing algo
    (see  ckan/src/ckanext-spatial/ckanext/spatial/harvesters/base.py L94)
    This also checks on the data-format iso values
    :param package:
    :return:
    """
    # get first the formats inferred by default:
    formats = dict_list_or_dict_reduce(package['resources'], 'format')
    # then get the data-format values
    data_formats = filter(lambda x: x['key'] == 'data-format', package.get('extras', []))
    data_formats = data_formats[0]['value'] if len(data_formats) > 0 else ''
    formats.extend(data_formats.split(','))
    # strip whitespaces around words and remove empty tags
    formats = [x.strip() for x in formats if x]
    #formats = [x for x in formats if x]
    # deduplicate list of values
    formats = list(set(formats))
    # sort alphabetically
    return sorted(formats)


def update_frequency_etalab_codelist(field):
    """
    Provides a choices list of update frequency values, matching the Etalab codelist (subset that has a match also in
    ISO 19139 codelist
    Used in scheming config ckan_dataset.json.
    :return:
    """
    # create a list of value/label entries to be used in the combobox in the dataset form
    return ({ 'value': x['eta_code'], 'label': x['label_fr'] } for x in update_frequencies)


# not used, finally. Might be removed...
def themes_codelist(field):
    """
    Provides a choices list of themes, matching the PIGMA list
    Used in scheming config ckan_dataset.json.
    :return:
    """
    # create a list of value/label entries to be used in the combobox in the dataset form
    return ({ 'value': k, 'label': v['label_fr'] } for k,v in themes.items())


def get_helpers():
    '''Register the functions above as a template helper functions.

    '''
    # Template helper function names should begin with the name of the
    # extension they belong to, to avoid clashing with functions from
    # other extensions.
    return {
        'theme_dict_list_or_dict_reduce': dict_list_or_dict_reduce,
        'theme_list_data_formats': list_data_formats,
        'theme_update_frequency_etalab_codelist' : update_frequency_etalab_codelist,
        'theme_themes_codelist' : themes_codelist
    }