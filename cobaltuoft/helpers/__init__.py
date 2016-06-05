import json
import os
import requests

from collections import OrderedDict
from datetime import datetime
from os.path import exists, isfile, realpath, dirname

from .scrapers import *

DATA_DIR = dirname(realpath(__file__)) + '/../data/'


def get(url, params=None, headers=None, verbose=False):
    """Make the request and return either the response or Exception."""
    res = None

    with requests.Session() as s:
        try:
            res = s.get(url=url, params=params, headers=headers, timeout=10)
        except requests.exceptions.RequestException as e:
            res = e  # raise e instead?

    return res


def validate_request_response(resp):
    """Return True iff resp returned an OK and is not an Exception."""
    return (resp and not
            (isinstance(resp, requests.exceptions.RequestException) or
             resp.status_code != 200))


def put_value(dict, key, fallback):
    return dict[key] if key in dict else fallback


def deep_convert_dict(obj):
    """Return the object after converting each OrderedDict to dict."""
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
    """Check if directory exists and create it, if not."""
    if not exists(directory):
        os.makedirs(directory)

    return exists(directory)


def get_active_apis():
    """Return the list of active APIs if they exist and are less than 5 days
    old, otherwise rescrape them."""

    file = DATA_DIR + '/active_apis.json'

    if not verify_dir_exists(DATA_DIR):
        return []

    if isfile(file):
        with open(file, 'r') as f:
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

    with open(file, 'w') as f:
        f.write(json.dumps(doc, indent=2))

    return doc['apis']


def get_filter_keys():
    """Return the list of filter keys if they exist and are less than 5 days
    old, otherwise rescrape them."""

    file = DATA_DIR + '/filter_keys.json'

    if not verify_dir_exists(DATA_DIR):
        return []

    if isfile(file):
        with open(file, 'r') as f:
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

    with open(file, 'w') as f:
        f.write(json.dumps(doc, indent=2))

    return doc['filters']
