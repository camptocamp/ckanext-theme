# coding: utf8
from flask import Blueprint
import geojson
import requests
from json import dumps
from collections import Counter

from ckan.plugins.toolkit import config
import ckan.plugins.toolkit as toolkit
from ckan.views.api import _finish_ok
import template_helpers

theme_api = Blueprint('theme_api', __name__)


def discriminate_results(response_dict):
    '''
    If necessary, add more information to the result so that the user can make unambiguous choices
    (ex. several communes can have the same name
    '''
    communes = (commune for commune in response_dict if commune['level'] == u'fr:commune')
    for commune in communes:
        try:
            postcode = commune['keys'].get('postal')[0]
            commune['name'] += ' ({})'.format(postcode)
        except:
            pass
    return response_dict


@theme_api.route('/theme-api/geoextent/name/autocomplete', endpoint='etalab_autocomplete_geog_entities')
def etalab_autocomplete_geog_entities():
    '''Autocomplete service, using data.gouv.fr API to get a list of administrative entities'''
    q = toolkit.request.args.get(u'incomplete', u'')
    limit = toolkit.request.args.get(u'size', 10)
    API_URI = config.get('ckanext.theme.api.geoextent.name.autocomplete.url')
    response = requests.get(API_URI.format(q, limit))
    assert response.status_code == 200
    response_dict = response.json()
    response_dict = discriminate_results(response_dict)
    resultSet = {
        u'ResultSet': {
            u'Result': response_dict
        }
    }
    return _finish_ok(resultSet)


@theme_api.route('/theme-api/geoextent/bbox', endpoint='etalab_autocomplete_bbox')
def etalab_get_extent_bbox():
    """
    Given the ID of an administrative service, uses data.gouv.fr API to retrieve its geometry
    then simplifies it and return just the bounding box (rectangle)
    If parameter geometry_type=contour is given, it returns the full geometry
    Else, it will return just the rectangular bounding box
    :return: bounding box in geojson
    """
    q = toolkit.request.args.get(u'id', u'')
    geometry_type = toolkit.request.args.get(u'geometry_type', u'box')
    API_URI = config.get('ckanext.theme.api.geoextent.bbox.url')
    response = requests.get(API_URI.format(q))
    assert response.status_code == 200
    response_dict = response.json()
    if not response_dict['geometry'].get('coordinates'):
        return ''

    if geometry_type == 'contour':
        return dumps(response_dict['geometry'])

    coords = list(geojson.utils.coords(response_dict['geometry']))
    poly = _bbox(coords)
    return geojson.dumps(poly)


@theme_api.route('/theme-api/update_frequency/list', endpoint='update_frequency_list')
def update_frequency_list():
    '''Provides the list of possible update_frequency values, according to etalab list'''
    values = list(template_helpers.update_frequency_etalab_codelist(None))
    resultSet = {
        u'ResultSet': {
            u'Result': values
        }
    }
    return _finish_ok(resultSet)


def _bbox(coord_list):
    box = []
    for i in (0, 1):
        res = sorted(coord_list, key=lambda x: x[i])
        box.append((res[0][i], res[-1][i]))
    #ret = f"({box[0][0]} {box[1][0]}, {box[0][1]} {box[1][1]})" # xmin, ymin, xmax, ymax
    poly = geojson.Polygon([[ (box[0][0], box[1][0]),
                              (box[0][0], box[1][1]),
                              (box[0][1], box[1][1]),
                              (box[0][1], box[1][0]),
                              (box[0][0], box[1][0])
                              ]])
    return poly