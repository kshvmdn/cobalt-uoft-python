from .endpoints import Endpoints
from .helpers import get, get_filter_keys


class Cobalt:
    def __init__(self, api_key=None):
        self.host = 'http://cobalt.qas.im/api/1.0'

        self.headers = {
            'Referer': 'https://pypi.python.org/pypi/cobaltuoft',
            'Authorization': api_key
        }

        if not api_key or not self._is_valid_key():
            raise ValueError('Expected valid API key.')

        self.filter_keys = get_filter_keys()

    def _get(self, url, params=None, headers=None):
        headers = headers or self.headers
        return get(url=url, params=params, headers=headers)

    def _is_valid_key(self):
        r = self._get(self.host)
        return r.reason == 'Not Found' and r.status_code == 404

    def _run(self, api, endpoint=None, params=None):
        res = Endpoints.run(api=api,
                            endpoint=endpoint,
                            params=params,
                            filter_keys=self.filter_keys[api],
                            get=self._get)
        return res.json()

    def athletics(self, endpoint=None, params=None):
        return self._run(api='athletics', endpoint=endpoint, params=params)

    def buildings(self, endpoint=None, params=None):
        return self._run(api='buildings', endpoint=endpoint, params=params)

    def courses(self, endpoint=None, params=None):
        return self._run(api='courses', endpoint=endpoint, params=params)

    def food(self, endpoint=None, params=None):
        return self._run(api='food', endpoint=endpoint, params=params)

    def textbooks(self, endpoint=None, params=None):
        return self._run(api='textbooks', endpoint=endpoint, params=params)
