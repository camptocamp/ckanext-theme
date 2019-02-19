# coding: utf8
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

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
        # Ajouter les filtres, dans l'ordre d'affichage sur la page
        return OrderedDict([
            ('organization', u'Organisations'),
            ('groups', u'Thématiques'),
            ('datatype', u'Types'),
            ('support', u'Supports'),
            ('res_format', u'Formats'),
            ('license_id', u'Licences'),
            ('tags', u'Mots-clés'),
            ('update_frequency', u'Fréquence de mise à jour'),
            ('granularity', u'Granularité de la couverture territoriale'),
            ])

    # IPackageController
    def before_index(self, pkg_dict):
        pkg_dict['datatype'] = loads(pkg_dict.get('datatype', '[]'))
        return pkg_dict
