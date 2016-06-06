from .helpers import put_value


class Response:
    """A class for API responses, with attributes for content and error."""

    def __init__(self, content=None, error=None, url=None):
        self.data, self.url = content, url
        self._set_error(error)

    def _set_error(self, error):
        """Set the error attribute, if it exists."""
        self.error = {
            'message': put_value(error, 'message', 'Request failed.'),
            'status_code': put_value(error, 'status', 400)
        } if isinstance(error, dict) and error != {} else None
