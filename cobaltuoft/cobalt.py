import requests

from .endpoint import Endpoint
from .helpers import get, get_filter_keys, validate_request_response
from .response import Response


class Cobalt:
    """A class for requesting data from the Cobalt web API."""

    def __init__(self, host='http://cobalt.qas.im/api/1.0', api_key=None):
        self.host = host

        self.headers = {
            'Referer': 'https://pypi.python.org/pypi/cobaltuoft',
            'Authorization': api_key
        }

        if not api_key or not self._is_valid_key():
            raise ValueError('Expected valid API key.')

        self.filter_keys = get_filter_keys()

    def _is_valid_key(self):
        """Determine if the provided API key is valid."""
        r = self._get(self.host)

        # Invalid keys throw a 400 with a different message
        return r.reason == 'Not Found' and r.status_code == 404

    def _get(self, url, params=None, headers=None):
        headers = headers or self.headers
        return get(url=url, params=params, headers=headers)

    def _run(self, api, endpoint=None, params=None):
        """Make a request to the API and parse the response body/error."""
        resp = Endpoint.run(api=api,
                            endpoint=endpoint,
                            params=params,
                            filter_keys=self.filter_keys[api],
                            get=self._get)

        data = url = err = None

        if not validate_request_response(resp) and resp:
            try:
                err.update({
                    'status': resp.status_code,
                    'message': resp.reason
                })
            except AttributeError:
                err['message'] = str(resp)
        elif resp:
            data, url = resp.json(), resp.url

        return Response(content=data, url=url, error=err)

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
