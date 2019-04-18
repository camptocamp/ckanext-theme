#!/usr/bin/env python
# coding: utf8
import urllib2
import urllib
import json
import pprint

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import Terminal256Formatter
from pprint import pformat


def pprint_color(obj):
    print highlight(pformat(obj), PythonLexer(), Terminal256Formatter())


API_URI = 'http://localhost:5001/api/3/'
AUTH_TOKEN = '006aa3b9-ffa3-4fca-ba80-caac60278681'
IMG_BASEURI = '/fanstatic/pigma_theme/:version:xxx/'

GROUPS = {
        "administration": u"Administration et action publique",
        "agriculture": u"Agriculture, sylviculture et pêche",
        "amenagement": u"Aménagement et urbanisme",
        "citoyennete": u"Citoyenneté et démocratie",
        "culture": u"Culture, patrimoine et tourisme",
        "economie": u"Économie et entreprises",
        "energie": u"Énergies et réseaux",
        "environnement": u"Environnement et climat",
        "equipement": u"Équipements, bâtiments et logement",
        "formation": u"Formation, éducation et emploi",
        "imagerie": u"Imagerie et occupation du sol",
        "limites-administratives": u"Limites administratives et réferentiels",
        "mer": u"Mer, littoral et montagne",
        "mobilite": u"Mobilité et transport",
        "sante": u"Sciences, recherche et innovation",
        "sciences": u"Social, santé et sports"}

dataset_dicts = [{
        "name": key,
        "title": label,
        "id": key + '2',
        "image_url": IMG_BASEURI + "{}.png".format(key)
    } for (key, label) in GROUPS.iteritems()]


for dataset_dict in dataset_dicts:
    request = urllib2.Request(API_URI + 'action/group_create')
    request.add_header('Authorization', AUTH_TOKEN)
    # import ipdb;ipdb.set_trace()
    response = urllib2.urlopen(request, urllib.quote(json.dumps(dataset_dict)))
    assert response.code == 200

    response_dict = json.loads(response.read())
    assert response_dict['success'] is True

    created_package = response_dict['result']
    pprint_color(created_package)


