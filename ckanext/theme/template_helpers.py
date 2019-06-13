# Template helper functions
from ckan.lib.helpers import dict_list_reduce

from harvest_helpers import update_frequencies

def dict_list_or_dict_reduce(list_, key, unique=True):
    """
    Hack to make helpers.dict_list_reduce work also if provided a dict of dicts instead of a list of dicts
    """
    if isinstance(list_, dict):
        list_ = list_.values()
    return dict_list_reduce(list_, key, unique)


def update_frequency_etalab_codelist(field):
    """
    Provides a choices list of update frequency values, matching the Etalab codelist (subset that has a match also in
    ISO 19139 codelist
    Used in scheming config ckan_dataset.json.
    :return:
    """
    # create a list of value/label entries to be used in the combobox in the dataset form
    return ({ 'value': x['eta_code'], 'label': x['label_fr'] } for x in update_frequencies)



def get_helpers():
    '''Register the functions above as a template helper functions.

    '''
    # Template helper function names should begin with the name of the
    # extension they belong to, to avoid clashing with functions from
    # other extensions.
    return {
        'theme_dict_list_or_dict_reduce': dict_list_or_dict_reduce,
        'theme_update_frequency_etalab_codelist' : update_frequency_etalab_codelist
    }