#!/usr/bin/env python
# coding: utf8
import argparse
import psycopg2
import urllib2
import urllib
import json
import ssl
import sys
from base64 import encodestring

global DB_CONNECT_STRING
DB_CONNECT_STRING="host=localhost dbname=ckan port=15432 user=ckan password=ckan"

def _get_harvested_then_lost_datasets(org, API_URI, API_KEY=None, BASE64AUTH=None, list_all=False):
    """
    Scan an org's datasets and try to guess which datasets were retrieved using harvesting, then lost from harvesting logs
    The context is the duplicates we get after harvesting for a while. The correspondance guid-id is lost and then, the
    datasets are still part of the org, but not attached to the harvester anymore. Those are the datasets we seek
    :param org: org name
    :return: a list of dicts, one dict per group
    """
    datasets = []
    datasets_duplicates = []
    datasets_OK = []

    # retrieve from DB the list of packages that are NOT tracked by the harvesters (ie not in harvest_object)
    sql_query = "SELECT id, name, owner_org FROM package WHERE type='dataset' AND package.id NOT IN (SELECT package_id FROM harvest_object WHERE package_id IS NOT NULL) "
    if org:
        sql_query += " AND owner_org = '" + org +"' "
    sql_query += " ORDER BY owner_org, name;"

    conn = psycopg2.connect(DB_CONNECT_STRING)
    cur = conn.cursor()
    cur.execute(sql_query)
    datasets = cur.fetchall()
    # inspect each dataset to estimate if it comes from harvesting or not.
    # we will look at the inspire_url key and check if it points to a geonetwork instance
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    for ds in datasets:
        data_values = {'id': ds[0] }
        data = urllib.quote(json.dumps(data_values))
        request = urllib2.Request(API_URI + 'action/package_show', data)
        _authenticate_request(request, API_KEY, BASE64AUTH)
        response = urllib2.urlopen(request)
        assert response.code == 200
        response_json = response.read()
        response_dict=json.loads(response_json)
        mtd = response_dict['result']
        geonetwork_url = mtd.get('inspire_url', mtd.get('hyperlink', ''))
        if 'geonetwork' in geonetwork_url:
            # keep it
            print("{}/{} \t\t duplicate (to remove)".format(ds[2], response_dict['result'].get('name')))
            datasets_duplicates.append(ds)
        else:
            datasets_OK.append(ds)
            if list_all:
                print("{}/{} \t\t don't touch".format(ds[2], response_dict['result'].get('name')))

    #datasets.sort(key=lambda ds: ds[2]+'_'+ds[1]) # sort by org + alphabetically    return datasets # done in SQL
    return datasets_duplicates, datasets_OK, datasets

def _authenticate_request(request, API_KEY=None, BASE64AUTH=None):
    if (API_KEY):
        request.add_header('X-CKAN-API-Key', API_KEY)
    else:
        request.add_header("Authorization", "Basic %s" % BASE64AUTH)


def _purge_datasets(datasets, API_URI, API_KEY=None, BASE64AUTH=None):
    """
    Purge datasets from the catalogue (be careful, no going back after a purge)
    :param dataset: list of (id, name) tuples.
    :param API_URI: URL to ckan api (e.g.https://georchestra.mydomain.org/ckan/api/3/)
    :param BASE64AUTH: basic auth chain built with user/passwd
    :return:
    """
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    for dataset in datasets:
        try:
            data_values = {'id': dataset[0] }
            data = urllib.quote(json.dumps(data_values))
            request = urllib2.Request(API_URI + 'action/dataset_purge', data)
            _authenticate_request(request, API_KEY, BASE64AUTH)
            response = urllib2.urlopen(request)
            assert response.code == 200
            print('purged {}'.format(dataset[1]) )
        except:
            print('error purging dataset {} ({})'.format(dataset[0], dataset[1]))


def main():
    # Input arguments
    parser = argparse.ArgumentParser(description='''
    Reads group configuration  in a CSV file dans creates them using CKAN's API. 
    You can provide your API key or user + password instead
    ''')
    parser.add_argument('ckan_api_url', help='the source name to process')
    parser.add_argument('-o', '--org',
                        help='organisation to clean')
    parser.add_argument('-a', '--all' , dest='list_all', action='store_true',
                        help='List all, including datasets that are not concerned')
    parser.set_defaults(list_all=False)
    parser.add_argument('--purge' , dest='purge', action='store_true',
                        help='Purge identified datasets')
    parser.set_defaults(purge=False)
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

    # List datasets
    duplicates, ok, ds = _get_harvested_then_lost_datasets(args.org, API_URI, API_KEY, BASE64AUTH, args.list_all)

    print("{} duplicates, {} datasets not related to a harvester".format(len(duplicates), len(ok)))
    if not duplicates:
        print("No duplicates. Good for you !")
        sys.exit(0)

    # Purge retained datasets
    if args.purge:
        _purge_datasets(duplicates, API_URI, API_KEY, BASE64AUTH)
        print("reset and re-run the harvest process. This should be fine now")


if __name__ == '__main__':
    main()