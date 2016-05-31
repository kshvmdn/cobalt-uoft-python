from .endpoints.courses import Courses
import requests


class Cobalt:
    def __init__(self, api_key=None):
        self.base_url = 'http://cobalt.qas.im/api/1.0'
        self.headers = {
            'Authorization': api_key
        }

        if not api_key or not self._is_valid_key(api_key):
            raise ValueError('Expected valid API key.')

    def _get(self, url, params=None):
        return requests.get(url=url, params=params, headers=self.headers)

    def _is_valid_key(self, key):
        payload = {'key': key}
        r = self._get(self.base_url, params=payload)
        return r.reason == 'Not Found' and r.status_code == 404

    def courses(self, endpoint=None, params=None):
        res = Courses.run(endpoint=endpoint, params=params, get=self._get)
        # print(res.url)
        return res.json()
