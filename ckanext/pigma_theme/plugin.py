# coding: utf8
from collections import OrderedDict
from json import loads
from os.path import join, dirname, abspath

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.plugins.toolkit import _
from ckanext.spatial.interfaces import ISpatialHarvester

import logging
log = logging.getLogger(__name__)


class Pigma_ThemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IFacets, inherit=True)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.ITranslation)
    plugins.implements(ISpatialHarvester, inherit=True)

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

mapping = {
        "administration": (
            u"Services d'utilité publique et services publics"
            ),
        "agriculture": (
            u"Installations agricoles et aquacoles"
            ),
        "amenagement": (
            u"Adresses",
            u"Zones de gestion, de restriction ou de réglementation et unités de déclaration"
            ),
        "economie": (
            u"Lieux de production et sites industriels"
            ),
        "energie": (
            u"Sources d'énergie"
            ),
        "environnement": (
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
        "equipement": (
            u"Bâtiments",
            u"Installations de suivi environnemental"
            ),
        "mer": (
            u"Régions maritimes",
            u"Caractéristiques géographiques océanographiques"
            ),
        "imagerie": (
            u"Ortho-imagerie",
            u"Occupation des terres",
            u"Parcelles cadastrales",
            u"Usage des sols"
            ),
        "limites-administratives": (
            u"Unités administratives",
            u"Unités statistiques",
            u"Dénominations géographiques"
            ),
        "mobilite": (
            u"Réseaux de transport"
            ),
        "sante": (
            u"Santé et sécurité des personnes",
            u"Répartition de la population-Démographie"
            )
        }
