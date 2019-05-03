#!/usr/bin/env python
# coding: utf8
from __future__ import print_function

import argparse
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

fields_catalog = {
    'ckan_fields': dict(),
    'extra_fields': dict(),
    'patched_fields' : dict(),
}

open_licence_tags = [
    "Aucune raison de restriction",
    "Licence Ouverte",
]

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def fetch(action, api_uri, api_key, base64auth, data=None):
    req = urllib2.Request(api_uri + action)
    req.add_header('X-CKAN-API-Key', api_key)
    req.add_header('Authorization', 'Basic %s' % base64auth)
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


def get_sub(pkg, key, sub_key_k, sub_value_k, id, default=''):
    sub = get(pkg, key)
    try:
        d = json.loads(sub)
        return next(item[sub_value_k] for item in d if id in item[sub_key_k])
    except:
        return default


def infer_datatypes(pkg):
    dt = []
    # Look for open source licence hints
    # TODO: if possible, be exhaustive...
    lic = get(pkg, 'access_constraints')
    if lic:
        lic_values = json.loads(lic)
        # see if lists intersect
        if list(set(open_licence_tags) & set(lic_values)):
            dt.append(u'donnees-ouvertes')

    # check resource type
    # TODO: identify the values for u'donnees-intelligentes' and u'rapports-etudes'
    type = get(pkg, 'resource-type')
    if type == 'dataset':
        dt.append(u'donnees-geographiques')

    return dt if dt else [u'donnees-geographiques'] # we need to provide at least one value


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


def _catalog_ingest(pkg, patch=None):
    """
    Add the content of pkg to the fields_catalog object. It lists the non-redundant values taken, for each field key,
    split between base fields, extras, patched values (conversion from extras to base)
    :param pkg:
    :param patch:
    :return:
    """
    for k, v in pkg.iteritems():
        # catalog ckan basic fields
        if k == 'extras':
            continue
        if not fields_catalog['ckan_fields'].get(k):
            fields_catalog['ckan_fields'][k] = [v]

        if v not in fields_catalog['ckan_fields'][k]:
            fields_catalog['ckan_fields'][k].append(v)

        # catalog extras
        if pkg.get('extras'):
            for d in pkg['extras']:
                # catalog extra fields
                if not fields_catalog['extra_fields'].get(d['key']):
                    fields_catalog['extra_fields'][d['key']] = [d['value']]

                if d['value'] not in fields_catalog['extra_fields'][d['key']]:
                    fields_catalog['extra_fields'][d['key']].append(d['value'])

        if patch:
            for k, v in patch.iteritems():
                # catalog extra fields
                if not fields_catalog['patched_fields'].get(k):
                    fields_catalog['patched_fields'][k] = [v]

                if v not in fields_catalog['patched_fields'][k]:
                    fields_catalog['patched_fields'][k].append(v)


def main():
    # Input arguments
    parser = argparse.ArgumentParser(description='''
    Reads group configuration  in a CSV file dans creates them using CKAN's API. GeOrchestra does not allow API keys, 
    so we use user/password instead
    ''')
    parser.add_argument('ckan_api_url', help='the source name to process')
    parser.add_argument('-k', '--api_key',
                        help='CKAN API key')
    parser.add_argument('-u', '--user',
            help='geOrchestra user name')
    parser.add_argument('-p', '--password',
            help='geOrchestra user password')
    parser.add_argument('--catalog_fields_create',
                        help='Create a catalog of fields. Give the file path as parameter')
    args = parser.parse_args()

    api_uri = args.ckan_api_url
    api_key = args.api_key
    BASE64AUTH = encodestring('%s:%s' % (args.user, args.password)).replace('\n', '')
    if not (api_uri):
        log.error("You need to provide api parameters")
        return

    packages = fetch('action/package_list', api_uri, api_key, BASE64AUTH)
    print('Got {} datasets'.format(len(packages)))

    for package in packages:
        print('Fetching «{}»'.format(package), end='')
        pkg = fetch('action/package_show?id={}'.format(package), api_uri, api_key, BASE64AUTH)
        if False:
            if args.catalog_fields_create:
                _catalog_ingest(pkg)
            print('… skipping')
            continue
        else:
            patch = {}
            patch['id'] = package
            patch['author'] = get_sub(pkg, 'responsible-party', 'roles', 'name', 'pointOfContact')
            patch['author_email'] = get(pkg, 'contact-email')
            patch['dataset_modification_date'] = get_sub(pkg, 'dataset-reference-date', 'type', 'value', 'creation')
            patch['dataset_publication_date'] = get_sub(pkg, 'dataset-reference-date', 'type', 'value', 'publication')
            patch['datatype'] = infer_datatypes(pkg)
            patch['extras'] = []
            patch['license_id'] = 'other-at'
            patch['maintainer_email'] = get(pkg, 'contact-email')
            patch['metadata_created'] = get(pkg, 'metadata-date')
            patch['metadata_modified'] = get(pkg, 'metadata-date')
            patch['resources'] = pkg['resources']
            patch['spatial'] = get(pkg, 'spatial')
            patch['tags'] = pkg['tags']
            patch['thumbnail'] = get(pkg, 'graphic-preview-file')
            patch['update_frequency'] = get(pkg, 'frequency-of-update', 'unknow')

            for tag in patch['tags']:
                tag['name'] = slugify(tag['name'])
            for resource in patch['resources']:
                if 'data_type' not in resource or resource['data_type'] == '':
                    resource['data_type'] = 'other'
                if 'description' not in resource or resource['description'] == '':
                    resource['description'] = 'Non renseigné'

            if args.catalog_fields_create:
                _catalog_ingest(pkg, patch)
            try:
                updated = fetch('action/package_patch', api_uri, api_key, BASE64AUTH, data=patch)
                print(' OK')
            except urllib2.HTTPError as e:
                print(' FAIL!')
                print(e.read())

    if args.catalog_fields_create:
        with open(args.catalog_fields_create, 'w') as outfile:
            json.dump(fields_catalog, outfile, indent=2, sort_keys=True)


if __name__ == '__main__':
    main()
