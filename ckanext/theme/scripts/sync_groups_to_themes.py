#!/usr/bin/env python
# coding: utf8
import argparse
import csv
import urllib2
import urllib
import json
import ssl
from base64 import encodestring

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import Terminal256Formatter
from pprint import pformat
import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)
pagination = 3

def pprint_color(obj):
    print highlight(pformat(obj), PythonLexer(), Terminal256Formatter())


def _authenticate_request(request, API_KEY=None, BASE64AUTH=None):
    if (API_KEY):
        request.add_header('X-CKAN-API-Key', API_KEY)
    else:
        request.add_header("Authorization", "Basic %s" % BASE64AUTH)


def _sync_groups_to_themes(API_URI, API_KEY=None, BASE64AUTH=None):
    """
    Iterates over the existing datasets. For every dataset, initialize the themes field with the values taken from the
    groups the dataset belongs to.
    :param API_URI: URL to ckan api (e.g.https://georchestra.mydomain.org/ckan/api/3/)
    :param BASE64AUTH: basic auth chain built with user/passwd
    :return:
    """
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    start_index = 0

    while True:
        pkg_list = list_packages(ctx, start_index, pagination, API_URI, API_KEY, BASE64AUTH)
        if pkg_list and ( len(pkg_list['results']) > 0 ):
            for pkg in pkg_list['results']:
                log.info("Working on package {}".format(pkg['name']))
                if len(pkg['groups']) > 0:
                    pkg['themes'] = [grp['name'] for grp in pkg['groups']]
                    patch = {
                        'id': pkg['id'],
                        'themes' : pkg['themes']
                    }
                    patch_package(patch, ctx, API_URI, API_KEY, BASE64AUTH)
        else:
            break
        start_index += pagination

    log.info("finished")

def list_packages(context, start, rows, API_URI, API_KEY=None, BASE64AUTH=None):
    pkg_list=None
    dataset_dict = {
        'start': start,
        'rows': rows,
        'include_private': True,
    }
    try:
        request = urllib2.Request(API_URI + 'action/package_search')
        response = urllib2.urlopen(request, urllib.quote(json.dumps(dataset_dict)), context=context)
        assert response.code == 200
        response_dict = json.loads(response.read())
        assert response_dict['success'] is True

        pkg_list = response_dict['result']
    except Exception as e:
        log.error("unable to list the packages")
        return None
    return pkg_list


def patch_package(patch_dict, context, API_URI, API_KEY=None, BASE64AUTH=None):
    try:
        request = urllib2.Request(API_URI + 'action/package_patch')
        _authenticate_request(request, API_KEY, BASE64AUTH)
        response = urllib2.urlopen(request, urllib.quote(json.dumps(patch_dict)), context=context)
        assert response.code == 200
        response_dict = json.loads(response.read())
        assert response_dict['success'] is True

        pkg = response_dict['result']
        log.info("patched package {}".format(pkg.get('name', '')))
        return response_dict['success']
    except Exception as e:
        log.error("unable to patch the package {}. Error message: {}".format(patch_dict.get('id', ''), e))
        return False


def main():
    # Input arguments
    parser = argparse.ArgumentParser(description='''
    Reads group configuration  in a CSV file dans creates them using CKAN's API. 
    You can provide your API key or user + password instead
    ''')
    parser.add_argument('ckan_api_url', help='the source name to process')
    parser.add_argument('-u', '--user',
                        help='geOrchestra user name')
    parser.add_argument('-p', '--password',
                        help='geOrchestra user password')
    parser.add_argument('-k', '--api_key',
                        help='ckan user\'s API key')
    args = parser.parse_args()

    API_URI = args.ckan_api_url
    BASE64AUTH = encodestring('%s:%s' % (args.user, args.password)).replace('\n', '')
    API_KEY = args.api_key

    #Create groups on CKAN
    _sync_groups_to_themes(API_URI, API_KEY, BASE64AUTH)


if __name__ == '__main__':
    main()