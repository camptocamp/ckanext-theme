#!/usr/bin/env python
# coding: utf8
from __future__ import print_function

import urllib2
import urllib
import json
import pprint
import ssl
import re
from base64 import encodestring

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import Terminal256Formatter
from pprint import pformat
from logging import getLogger
log = getLogger(__name__)

API_URI = 'http://localhost:5001/api/3/'
AUTH_TOKEN = '006aa3b9-ffa3-4fca-ba80-caac60278681'
BASE64AUTH = encodestring('%s:%s' % ('aabt', 'truitetruite')).replace('\n', '')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch(action, data=None):
    req = urllib2.Request(API_URI + action)
    req.add_header('Authorization', AUTH_TOKEN)
    if data is not None:
        response = urllib2.urlopen(req, urllib.quote(json.dumps(data)), context=ctx)
    else:
        response = urllib2.urlopen(req, context=ctx)
    assert response.code == 200
    json_response =  json.loads(response.read())
    assert json_response['success'] is True
    return json_response['result']

def get(pkg, key, default=''):
    val = filter(lambda x: x['key'] == key, pkg.get('extras', []))
    val = val[0]['value'] if len(val) > 0 else ''
    return val or default

def slugify(s):
    """
    Simplifies ugly strings into something URL-friendly.
    >>> print slugify("[Some] _ Article's Title--")
    some-articles-title
    """
    # "[Some] _ Article's Title--"
    # "[some] _ article's title--"
    s = s.lower()
    # "[some] _ article's_title--"
    # "[some]___article's_title__"
    for c in [' ', '-', '.', '/']:
        s = s.replace(c, '_')
    # "[some]___article's_title__"
    # "some___articles_title__"
    s = re.sub('\W', '', s)
    # "some___articles_title__"
    # "some   articles title  "
    s = s.replace('_', ' ')
    # "some   articles title  "
    # "some articles title "
    s = re.sub('\s+', ' ', s)
    # "some articles title "
    # "some articles title"
    s = s.strip()
    # "some articles title"
    # "some-articles-title"
    s = s.replace(' ', '-')
    return s

packages = fetch('action/package_list')
print('Got {} datasets'.format(len(packages)))
for package in packages:
    print('Fectching «{}»'.format(package), end='')
    pkg = fetch('action/package_show?id={}'.format(package))
    if 'update_frequency' in pkg:
        print('… skipping')
        continue
    else:
        patch = {}
        patch['id'] = package
        patch['update_frequency'] = get(pkg, 'frequency-of-update', 'unknow')
        patch['spatial'] = get(pkg, 'spatial')
        patch['license_id'] = 'other-at'
        patch['datatype'] = 'unknown'
        patch['extras'] = []
        patch['resources'] = pkg['resources']
        patch['tags'] = pkg['tags']
        for tag in patch['tags']:
            tag['name'] = slugify(tag['name'])
        for resource in patch['resources']:
            if 'data_type' not in resource or resource['data_type'] == '':
                resource['data_type'] = 'other'
            if 'description' not in resource or resource['description'] == '':
                resource['description'] = 'Non renseigné'
        try:
            updated = fetch('action/package_patch', data=patch)
            print(' OK')
        except urllib2.HTTPError as e:
            print(' FAIL!')
            print(e.read())



