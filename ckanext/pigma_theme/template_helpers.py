# Template helper functions
from ckan.lib.helpers import dict_list_reduce


def dict_list_or_dict_reduce(list_, key, unique=True):
    """
    Hack to make helpers.dict_list_reduce work also if provided a dict of dicts instead of a list of dicts
    """
    if isinstance(list_, dict):
        list_ = list_.values()
    return dict_list_reduce(list_, key, unique)
