from collections import OrderedDict
from pprint import pprint
from .helpers import get

import json


class Datasets:
    API_URL = 'https://api.github.com/repos/cobalt-uoft/datasets'

    @staticmethod
    def _get(url, params=None):
        return get(url=url, params=params, headers={
            'Referer': 'https://github.com/'
        })

    @staticmethod
    def _get_tags():
        resp = Datasets._get(url='%s/tags' % Datasets.API_URL)
        return list(map(lambda tag: tag['name'], resp.json()))

    @staticmethod
    def _get_available_datasets(tag):
        resp = Datasets._get(url='%s/contents' % Datasets.API_URL,
                             params={'ref': tag})

        datasets = []

        for file in resp.json():
            if '.json' in file['name']:
                datasets.append((file['name'], file['download_url']))

        return datasets

    @staticmethod
    def _parse_cobalt_json(json_string):
        docs = []

        for doc in json_string.strip().split('\n'):
            try:
                docs.append(json.loads(doc, object_pairs_hook=OrderedDict))
            except e:
                pass

        return docs

    @staticmethod
    def run(tag='latest'):
        if tag not in Datasets._get_tags():
            raise ValueError('Unexpected tag value. Refer to this: ' +
                             'https://api.github.com/repos/cobalt-uoft/datasets/tags ' +
                             'for a list of valid tags.')

        if not tag or tag not in Datasets._get_tags() or tag == 'latest':
            tag = 'master'

        docs = {}

        for dataset, url in Datasets._get_available_datasets(tag):
            resp = Datasets._get(url=url)

            if resp.status_code != 200:
                continue

            docs[dataset.replace('.json', '')] = \
                Datasets._parse_cobalt_json(resp.text)

        return docs
