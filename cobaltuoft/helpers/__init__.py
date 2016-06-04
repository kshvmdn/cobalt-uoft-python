import json
import requests

from collections import OrderedDict
from datetime import datetime
from os.path import exists, isfile

from .scrapers import *


def get(url, params=None, headers=None):
    with requests.Session() as s:
        return s.get(url=url, params=params, headers=headers)


def deep_convert_dict(obj):
    converted = obj

    if isinstance(obj, OrderedDict):
        converted = dict(obj)
    elif isinstance(obj, list):
        converted = [deep_convert_dict(x) for x in obj]

    try:
        for k, v in converted.items():
            converted[k] = deep_convert_dict(v)
    except AttributeError:
        pass

    return converted


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
        'filters': scrape_filter_keys(get_active_apis()),
        'meta': {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    }

    with open('./data/filter_keys.json', 'w') as f:
        f.write(json.dumps(doc, indent=2))

    return doc['filters']
