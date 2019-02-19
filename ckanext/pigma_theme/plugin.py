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
            ('organization', _(u'Organisations')),
            ('groups', _(u'Thématiques')),
            ('datatype', _(u'Types')),
            ('support', _(u'Supports')),
            ('res_format', _(u'Formats')),
            ('license_id', _(u'Licences')),
            ('tags', _(u'Mots-clés')),
            ('update_frequency', _(u'Fréquence de mise à jour')),
            ('granularity', _(u'Granularité de la couverture territoriale')),
            ])

    # IPackageController
    def before_index(self, pkg_dict):
        pkg_dict['datatype'] = loads(pkg_dict.get('datatype', '[]'))
        return pkg_dict
