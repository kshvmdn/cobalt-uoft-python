from .helpers import put_value


class Response:
    def __init__(self, body=None, error=None, url=None):
        self.body, self.url = body, url
        self._set_error(error)

    def _set_error(self, error):
        self.error = {
            'message': put_value(error, 'message', 'Request failed.'),
            'status_code': put_value(error, 'status', 400)
        } if isinstance(error, dict) and error != {} else None
