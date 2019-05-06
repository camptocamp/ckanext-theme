# Template helper functions
from ckan.lib.helpers import dict_list_reduce, Page


def dict_list_or_dict_reduce(list_, key, unique=True):
    """
    Hack to make helpers.dict_list_reduce work also if provided a dict of dicts instead of a list of dicts
    """
    if isinstance(list_, dict):
        list_ = list_.values()
    return dict_list_reduce(list_, key, unique)

def filter_orgs(orgs_list):
    """
    filter org list of dict based on a critierd, default, orgs with at least one datatset
    """
    return list(filter(lambda x: x['package_count'] > 0, orgs_list))

def filtered_pager(orgs):
    """
    return a new Page instance. since Page class init a lot a stuff in __init__ this is needed. We can't recompute member.
    This function lacks options.
    """
    return Page(orgs)
