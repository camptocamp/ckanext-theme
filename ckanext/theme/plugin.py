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

    def after_map(self, map):
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
            ('organization', _(u'Organization')),
            ('groups', _(u'Group')),
            ('tags', _(u'Keyword')),

            ('res_format', _(u'Format')),
            ('accrualPeriodicity', _(u'Update frequency')),
            # ('datatype', _(u'Type')),
            # ('tags', _(u'Mot-clé')),
        ])

    # IPackageController
    def before_index(self, pkg_dict):
        pkg_dict['datatype'] = loads(pkg_dict.get('datatype', '[]'))
        return pkg_dict

    # IPackageController
    def after_update(self, context, pkg_dict):
        return self.themes_field_to_groups(context, pkg_dict)

    # IPackageController
    def after_create(self, context, pkg_dict):
        return self.themes_field_to_groups(context, pkg_dict)

    def themes_field_to_groups(self, context, pkg_dict):
        # assign groups based on the edition form's themes values (I couldn't manage a way to edit directly the groups)
        # 1. retrieve current groups list
        pkg = toolkit.get_action('package_show')(context, {'id': pkg_dict['id']})
        current_groups_names_list = [grp['name']for grp in pkg['groups']]
        # 2. build the themes list
        themes = loads(pkg_dict.get('themes', '[]'))
        # 3. if the difference is not null, update the groups the package belongs to
        # we need to perform this action as superuser, since I couldn't find a way to override auth system that would
        # work here...
        # This should be fine, since if we are there, it means we were allowed first to update this package
        user = toolkit.get_action('get_site_user')({'ignore_auth': True}, {})
        # we check if the groups list and themes list are different. In that case, we update only on the intersection
        # with available groups list (prevent possible mistakes in groups names)
        if bool(set(themes).symmetric_difference(current_groups_names_list)):
            all_groups_list = toolkit.get_action('group_list')(context, {})
            grps = [{'name' : theme} for theme in set(themes).intersection(all_groups_list)]
            updated_ds = toolkit.get_action('package_patch')({'user': user['name']}, data_dict={
                'id' : pkg_dict['id'],
                'groups' : grps
            })

        return {
            'context' : context,
            'pkg_dict': pkg_dict
        }

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
        try:
            harvest_helpers.fix_harvest_scheme_fields(package_dict, data_dict)
        except Exception as e:
            log.error('Error during improved harvesting of dataset {}. Raised exception {}'.format(package_dict['name'], e))
        return package_dict

    # ITemplateHelper
    def get_helpers(self):
        return theme_get_template_helpers()