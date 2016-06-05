import json

from collections import OrderedDict
from os.path import splitext

from .helpers import get, deep_convert_dict, validate_request_response
from .response import Response


class Datasets:
    """A class for requesting data from the Cobalt datasets.

    Datasets are hosted on GitHub @ http://github.com/cobalt-uoft/datasets."""

    GH_API = 'https://api.github.com'
    API_URL = '%s/repos/cobalt-uoft/datasets' % GH_API

    @staticmethod
    def _get(url, params=None):
        resp = get(url=url, params=params, headers={
            'Referer': Datasets.GH_API
        })

        if not validate_request_response(resp):
            return Datasets._prepare_response(resp, True)

        return resp

    @staticmethod
    def _get_tags():
        """Get a list of the available tags from the datasets repository."""
        resp = Datasets._get(url='%s/tags' % Datasets.API_URL)
        return list(map(lambda tag: tag['name'], resp.json()))

    @staticmethod
    def _get_available_datasets(tag):
        """Get a list of the available datasets for the provided tag."""
        resp = Datasets._get(url='%s/contents' % Datasets.API_URL, params={'ref': tag})

        datasets = {}

        for file in resp.json():
            if '.json' in file['name']:
                datasets[splitext(file['name'])[0]] = {
                    'name': file['name'],
                    'url': file['download_url']
                }

        return datasets

    @staticmethod
    def _parse_cobalt_json(json_string):
        """Convert Cobalt JSON to a Python dictionary."""
        docs = []

        for doc in json_string.strip().split('\n'):
            try:
                docs.append(json.loads(doc, object_pairs_hook=OrderedDict))
            except e:
                pass

        return deep_convert_dict(docs)

    @staticmethod
    def _prepare_response(resp, is_error=False):
        """Prepare a Response for an error if is_error or the dataset docs."""
        data = err = None

        if is_error and resp is not None:
            err = {}

            try:
                err.update({
                    'status': resp.status_code,
                    'message': resp.reason
                })
            except AttributeError:
                err['message'] = str(resp)
        elif resp:
            data = resp

        return Response(content=data, error=err)

    @staticmethod
    def run(tag='latest', datasets='*'):
        """Return a Response with a list of datasets for the provided tag."""
        tag = None if tag is None else tag.lower()

        if not tag or tag == 'latest':
            tag = 'master'

        if tag != 'master' and tag not in Datasets._get_tags():
            raise ValueError('Unexpected tag value. Refer to this: ' +
                             'https://api.github.com/repos/cobalt-uoft/datasets/tags ' +
                             'for a list of valid tags.')

        available_datasets = Datasets._get_available_datasets(tag)

        if not datasets:
            raise ValueError('Unexpected None `datasets` value.')
        elif datasets == '*':
            datasets = available_datasets.keys()
        elif type(datasets) != list:
            datasets = [datasets]

        datasets = [ds.lower() for ds in datasets]

        docs = {}

        for name, doc in available_datasets.items():
            if name not in datasets:
                continue

            resp = Datasets._get(url=doc['url'])

            docs[name] = Datasets._parse_cobalt_json(resp.text)

        return Datasets._prepare_response(docs)
