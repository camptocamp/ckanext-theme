# coding: utf8
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from collections import OrderedDict


class Pigma_ThemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IFacets, inherit=True)

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
