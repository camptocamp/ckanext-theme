# coding: utf8
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.plugins.toolkit import _

from collections import OrderedDict
from json import loads


class Pigma_ThemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IFacets, inherit=True)
    plugins.implements(plugins.IPackageController, inherit=True)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'pigma_theme')

    # IFacets
    def dataset_facets(self, facets_dict, package_type):
        return OrderedDict([
            ('groups', _(u'Themes')),
            ('keywords', _(u'Keywords')),
            ('datatype', _(u'Types')),
            ('update_frequency', _(u'Update frequency')),
            ('granularity', _(u'Granularity')),
            ('organization', _(u'Organizations')),
            # ('support', _(u'Supports')),
            # ('res_format', _(u'Formats')),
            # ('license_id', _(u'Licences')),
            # ('tags', _(u'Mots-clés')),
              ])


    # IPackageController
    def before_index(self, pkg_dict):
        pkg_dict['datatype'] = loads(pkg_dict.get('datatype', '[]'))
        return pkg_dict
