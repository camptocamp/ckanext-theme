#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# The following snippet creates a new package using the API, adding the package to the themes defined in the themes
# field
# You can of course add more optional fields, see ckan_dataset.json file for fields list
# Be sure to adjust the CKAN_URL and CKAN_API_KEY (use your API key)
# Beware that you can publish twice a dataset with same name, it will be errored as Conflict (even deleted, the dataset
# is still in the database, you need to purge it before you can publish it again using this script. Purging dataset
# is a functionality reserved to sysadmins

import urllib2
import urllib
import json
import pprint

CKAN_URL = 'https://georchestra.mydomain.org/datanouvelleaquitaine'
CKAN_API_KEY = '68843c2b-dea5-4b2a-9dfb-200ff80e8499'

dataset_dict = {
    'title' : 'Ile de Ré : Ecluses actuelles à poissons',
    'name' : 'ile-de-re-ecluses-actuelles-a-poissons',
    'tags': [
        {'name': 'Nouvelle Aquitaine'},
        {'name': 'donnees-ouvertes'},
        {'name': 'poissons'},
        {'name': 'écluses'},
        {'name': 'île de Ré'},
     ],
    'license_id': 'other-at',
    'owner_org': 'universite_la_rochelle',
    'notes': 'Cartographie des écluses à poissons actuellement encore en place sur l\'île de Ré',
    'update_frequency': 'unknown',
    'datatype': ["donnees-geographiques"],
    'themes': ['agriculture', 'mer', 'culture'],
}
# Use the json module to dump the dictionary to a string for posting.
data_string = urllib.quote(json.dumps(dataset_dict))

# We'll use the package_create function to create a new dataset.
request = urllib2.Request(
    CKAN_URL + '/api/3/action/package_create')

# Creating a dataset requires an authorization header.
# Replace *** with your API key, from your user account on the CKAN site
# that you're creating the dataset on.

# Use this if CKAN is accessed behind securit-proxy (geOrchestra use case)
request.add_header('X-CKAN-API-Key', CKAN_API_KEY)
# Use this if CKAN is accessed directly (not in geOrchestra)
#request.add_header('Authorization', CKAN_API_KEY)

# Make the HTTP request.
response = urllib2.urlopen(request, data_string)
assert response.code == 200

# Use the json module to load CKAN's response into a dictionary.
response_dict = json.loads(response.read())
assert response_dict['success'] is True

# package_create returns the created package as its result.
created_package = response_dict['result']
pprint.pprint(created_package)
