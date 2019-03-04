# coding: utf8
from collections import OrderedDict
from json import loads
from os.path import join, dirname, abspath

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.plugins.toolkit import _


class Pigma_ThemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IFacets, inherit=True)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.ITranslation)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'pigma_theme')

    # IFacets
    def dataset_facets(self, facets_dict, package_type):
        return OrderedDict([
            ('groups', _(u'Thèmes')),
            ('keywords', _(u'Mot-clefs')),
            ('datatype', _(u'Types')),
            ('update_frequency', _(u'Fréquence de mise à jour')),
            ('granularity', _(u'Granularité')),
            ('organization', _(u'Organisations')),
            # ('support', _(u'Supports')),
            # ('res_format', _(u'Formats')),
            # ('license_id', _(u'Licences')),
            # ('tags', _(u'Mots-clés')),
            ])

    # IPackageController
    def before_index(self, pkg_dict):
        pkg_dict['datatype'] = loads(pkg_dict.get('datatype', '[]'))
        return pkg_dict

    # ITranslation
    def i18n_locales(self):
        return ('fr')

    # ITranslation
    def i18n_directory(self):
        return join(dirname(abspath(__file__)), 'i18n')

    # ITranslation
    def i18n_domain(self):
        return 'ckanext-pigma_theme'
