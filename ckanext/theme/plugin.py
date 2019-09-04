# coding: utf8
from collections import OrderedDict
from json import loads
from os.path import join, dirname, abspath

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.plugins.toolkit import _
from ckanext.theme.template_helpers import get_helpers as theme_get_template_helpers
from ckanext.spatial.interfaces import ISpatialHarvester
import ckanext.theme.api as api
import ckanext.theme.config as config
import ckanext.theme.harvest_helpers as harvest_helpers


import logging

log = logging.getLogger(__name__)


class ThemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IRoutes)
    plugins.implements(plugins.IFacets, inherit=True)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.ITranslation)
    plugins.implements(ISpatialHarvester, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)

    # IBlueprint
    def get_blueprint(self):
        return api.theme_api

    # IRoutes
    def before_map(self, map):
        # sort organizations by default
        map.connect('ckanext_theme_organizations_index', '/organization?q=&sort=package_count+desc', action='index')
        return map

    def after_map(selfself, map):
        return map

    # Iconfigurable
    def configure(self, main_config):
        theme_config = config.configure(main_config)
        main_config.update(theme_config)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'theme')

    # IFacets
    def dataset_facets(self, facets_dict, package_type):
        return OrderedDict([
            ('groups', _(u'Groups')),
            ('tags', _(u'Mots-clés')),
            ('datatype', _(u'Types')),
            ('update_frequency', _(u'Fréquence de mise à jour')),
            ('granularity', _(u'Granularité')),
            ('organization', _(u'Organisations')),
            # ('support', _(u'Supports')),
            # ('res_format', _(u'Formats')),
            # ('license_id', _(u'Licences')),
        ])

    # IPackageController
    def before_index(self, pkg_dict):
        #pkg_dict['datatype'] = loads(pkg_dict.get('datatype', '[]'))
        return pkg_dict

    # IPackageController
    def before_search(self, search_param):
        search_param['qf'] = 'title^2 text'
        return search_param

    # ITranslation
    def i18n_locales(self):
        return ('fr')

    # ITranslation
    def i18n_directory(self):
        return join(dirname(abspath(__file__)), 'i18n')

    # ITranslation
    def i18n_domain(self):
        return 'ckanext-theme'

    # ISpatialHarvester
    def get_package_dict(self, context, data_dict):
        package_dict = data_dict['package_dict']
        iso_values = data_dict['iso_values']
        # log.debug(iso_values)
        log.info('Working on dataset {}'.format(package_dict['name']))
        # fix harvested package to make it compatible with the scheming extension
        # & transform geonetwork metadata to make them available in the schema
        harvest_helpers.fix_harvest_scheme_fields(package_dict, data_dict)
        return package_dict

    # ITemplateHelper
    def get_helpers(self):
        return theme_get_template_helpers()
