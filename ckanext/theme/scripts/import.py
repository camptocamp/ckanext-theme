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


def pprint_color(obj):
    print highlight(pformat(obj), PythonLexer(), Terminal256Formatter())


def _groups_from_csv(path):
    """
    Read a CSV file defining the groups to create
    :param path: path to the csv file (local, does not handle URLs)
    :return: a list of dicts, one dict per group
    """
    dataset_dicts = []
    with open(path, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        # This skips the first row of the CSV file.
        next(reader)
        for row in reader:
            row_as_dict = {
                "name": row[0],
                "title": row[1],
                "id": row[0],
                "image_url": row[2]
            }
            dataset_dicts.append(row_as_dict)
    return dataset_dicts


def _authenticate_request(request, API_KEY=None, BASE64AUTH=None):
    if (API_KEY):
        request.add_header('X-CKAN-API-Key', API_KEY)
    else:
        request.add_header("Authorization", "Basic %s" % BASE64AUTH)


def _create_groups(dataset_dicts, API_URI, API_KEY=None, BASE64AUTH=None):
    """
    Given a list of dicts defining the groups, creates the group using CKAN's API
    Since geOrchestra, for now, doesn't let in using the API key, we use basic auth.
    If a group already exists in CKAN, pruges it before creating it again.
    :param dataset_dicts:
    :param API_URI: URL to ckan api (e.g.https://georchestra.mydomain.org/ckan/api/3/)
    :param BASE64AUTH: basic auth chain built with user/passwd
    :return:
    """
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    for dataset_dict in dataset_dicts:
        try:
            delete_req = urllib2.Request(API_URI + 'action/group_purge')
            _authenticate_request(delete_req, API_KEY, BASE64AUTH)
            del_response = urllib2.urlopen(delete_req, urllib.quote(json.dumps(dataset_dict)), context=ctx)
            assert del_response.code == 200
        except:
            print('group {} did not exist before'.format(dataset_dict['id']))

        request = urllib2.Request(API_URI + 'action/group_create')
        _authenticate_request(request, API_KEY, BASE64AUTH)
        response = urllib2.urlopen(request, urllib.quote(json.dumps(dataset_dict)), context=ctx)
        assert response.code == 200

        response_dict = json.loads(response.read())
        assert response_dict['success'] is True

        created_package = response_dict['result']
        pprint_color(created_package)


def main():
    # Input arguments
    parser = argparse.ArgumentParser(description='''
    Reads group configuration  in a CSV file dans creates them using CKAN's API. 
    You can provide your API key or user + password instead
    ''')
    parser.add_argument('ckan_api_url', help='the source name to process')
    parser.add_argument('-c', '--csv',
                        help='csv file path')
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

    # Parse CSV
    dataset_dicts = _groups_from_csv(args.csv)
    #Create groups on CKAN
    _create_groups(dataset_dicts, API_URI, API_KEY, BASE64AUTH)


if __name__ == '__main__':
    main()