import requests
import json
import os.path
from datetime import datetime
from os.path import exists, isfile

from .scrapers import *


def get(url, params=None, headers=None):
    return requests.get(url=url, params=params, headers=headers)


def verify_dir_exists(directory):
    if not exists(directory):
        os.makedirs(directory)

    return exists(directory)


def get_active_apis():
    if not verify_dir_exists('./data'):
        return []

    if isfile('./data/active_apis.json'):
        with open('./data/active_apis.json', 'r') as f:
            doc = json.loads(f.read())

        write_date = datetime.strptime(doc['meta']['date'],
                                       '%Y-%m-%d %H:%M:%S')

        # Rescrape if previous data is more than 5 days old
        if (datetime.now() - write_date).seconds <= 432000:
            return doc['apis']

    doc = {
        'apis': scrape_apis(),
        'meta': {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    }

    with open('./data/active_apis.json', 'w') as f:
        f.write(json.dumps(doc, indent=2))

    return doc['apis']


def get_filter_keys():
    if not verify_dir_exists('./data'):
        return []

    if isfile('./data/filter_keys.json'):
        with open('./data/filter_keys.json', 'r') as f:
            doc = json.loads(f.read())

        write_date = datetime.strptime(doc['meta']['date'],
                                       '%Y-%m-%d %H:%M:%S')

        # Rescrape if previous data is more than 5 days old
        if (datetime.now() - write_date).seconds <= 432000:
            return doc['filters']

    doc = {
        'filters': scrape_filters(get_active_apis()),
        'meta': {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    }

    with open('./data/filter_keys.json', 'w') as f:
        f.write(json.dumps(doc, indent=2))

    return doc['filters']
