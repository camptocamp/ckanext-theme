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
    plugins.implements(plugins.IFacets, inherit=True)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.ITranslation)
    plugins.implements(ISpatialHarvester, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)

    # IBlueprint
    def get_blueprint(self):
        return api.theme_api

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
            ('organization', _(u'Organisation')),
            ('groups', _(u'Thématique')),
            ('keywords', _(u'Mot-clé')),

            ('granularity', _(u'Granularité')),
            ('res_format', _(u'Format')),
            ('update_frequency', _(u'Fréquence de mise à jour')),
            ('license_id', _(u'Licence')),
            # ('datatype', _(u'Type')),
            # ('tags', _(u'Mot-clé')),
        ])

    # IPackageController
    def before_index(self, pkg_dict):
        pkg_dict['datatype'] = loads(pkg_dict.get('datatype', '[]'))
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

        # Manage themes:
        #  * if there is [1..n] ISO themes, it is mapped to a pigma theme
        #  * else, if there is [1..n] inspire theme keywords, we try the mapping with them
        # Themes are managed as ckan groups
        package_dict['groups'] = harvest_helpers.get_themes(iso_values)

        package_dict['extras'].extend([
            {'key': 'inspire-url', 'value': harvest_helpers.gn_csw_build_inspire_link(data_dict['harvest_object'].source,
                                                                      iso_values)},
            {'key': 'topic-categories', 'value': ', '.join(iso_values.get('topic-category'))},
            {'key': 'data-format', 'value': ', '.join(f['name'] for f in iso_values.get('data-format'))},
        ])

        # TODO: check how the harvester identifies the format for the associated resources. Seems not to be very good
        # (only gets KMZ and HTML, does not get CSV, ESRI, DWG for instance look at layer 'Courbes de niveau (MNT) sur Bordeaux Métropole (La Cub) en 2001')
        # see code in /home/jean/dev/C2C/docker-ckan/ckan/src/ckanext-spatial/ckanext/spatial/harvesters/base.py L94

        # set a consistent point of contact (name & email match a same entity instead of random-ish)
        poc = harvest_helpers.get_poc(iso_values)
        if poc:
            harvest_helpers.update_or_set_extra(package_dict, 'contact', poc.get('organisation-name',
                                                                                 poc.get('individual-name', '')))
            harvest_helpers.update_or_set_extra(package_dict, 'contact-email', poc.get('contact-info').get('email', ''))

        return package_dict

    # ITemplateHelper
    def get_helpers(self):
        return theme_get_template_helpers()
<<<<<<< HEAD


# Note that mapping misses culture & education-formation groups
mapping = {
    "institutions-partenariats": (
        u"Services d'utilité publique et services publics"
    ),
    "amenagement": (
        u"Adresses",
        u"Zones de gestion, de restriction ou de réglementation et unités de déclaration"
    ),
    "economie-emploi": (
        u"Lieux de production et sites industriels"
    ),
    "reseaux-energies": (
        u"Sources d'énergie"
    ),
    "environnement-risques-sante": (
        u"Régions biogéographiques",
        u"Habitats et biotopes",
        u"Répartition des espèces",
        u"Conditions atmosphériques",
        u"Caractéristiques géographiques météorologiques",
        u"Sites protégés",
        u"Sols",
        u"Géologie",
        u"Ressources minérales",
        u"Zones à risque naturel",
        u"Altitude",
        u"Hydrographie"
    ),
    "donnees-reference": (
        u"Unités administratives",
        u"Unités statistiques",
        u"Dénominations géographiques"
    ),
    "transports-mobilites": (
        u"Réseaux de transport"
    )
}
=======
>>>>>>> e51e789... [GSKAN-224] Manage Themes + data format tags
