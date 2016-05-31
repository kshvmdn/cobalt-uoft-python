import requests
import json

from .endpoints import Endpoints
from .utils.scrape_filters import main as scrape_filters 


class Cobalt:
    def __init__(self, api_key=None):
        self.host = 'http://cobalt.qas.im/api/1.0'

        self.headers = {
            'Referer': 'Cobalt-UofT-Python'
        }

        if not api_key or not self._is_valid_key(api_key):
            raise ValueError('Expected valid API key.')

        self.headers['Authorization'] = api_key

        self.filter_map = scrape_filters() 

    def _get(self, url, params=None):
        return requests.get(url=url, params=params, headers=self.headers)

    def _is_valid_key(self, key):
        payload = {'key': key}
        r = self._get(self.host, params=payload)
        return r.reason == 'Not Found' and r.status_code == 404

    def _run(self, api, endpoint=None, params=None):
        res = Endpoints.run(api=api,
                            endpoint=endpoint,
                            params=params,
                            map=self.filter_map[api],
                            get=self._get)
        return res.json()

    def courses(self, endpoint=None, params=None):
        return self._run(api='courses', endpoint=endpoint, params=params)

    def buildings(self, endpoint=None, params=None):
        return self._run(api='buildings', endpoint=endpoint, params=params)
