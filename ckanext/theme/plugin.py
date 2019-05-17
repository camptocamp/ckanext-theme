# coding: utf8
from collections import OrderedDict
from json import loads
from os.path import join, dirname, abspath

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.plugins.toolkit import _
from ckanext.theme.template_helpers import dict_list_or_dict_reduce
from ckanext.spatial.interfaces import ISpatialHarvester

import logging

log = logging.getLogger(__name__)


class ThemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IFacets, inherit=True)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.ITranslation)
    plugins.implements(ISpatialHarvester, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)


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

        groups = []
        for group, keywords in mapping.iteritems():
            for keyword in iso_values.get('keyword-inspire-theme'):
                if keyword in keywords:
                    groups.append({'id': group})
        package_dict['groups'] = list(groups)

        return package_dict

    # ITemplateHelper
    def get_helpers(self):
        '''Register the most_popular_groups() function above as a template
        helper function.

        '''
        # Template helper function names should begin with the name of the
        # extension they belong to, to avoid clashing with functions from
        # other extensions.
        return {
            'dict_list_or_dict_reduce': dict_list_or_dict_reduce
        }


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
