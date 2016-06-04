class Endpoints:
    host = 'http://cobalt.qas.im/api/1.0'

    @staticmethod
    def run(api, get, endpoint=None, params=None, filter_keys=None):
        endpoint = Endpoints._parse_endpoint(endpoint)

        url, params = Endpoints._parse_url(api, endpoint, params), \
            Endpoints._parse_params(endpoint, params, filter_keys)

        return get(url=url, params=params)

    @staticmethod
    def _process_filter(queries, filter_keys=None):
        if (type(queries) == str):
            return queries

        a = []
        for filter in queries:
            o = []
            for k, v in filter:
                if filter_keys and k.lower() not in filter_keys:
                    continue
                o.append('%s:%s' % (k, v))
            a.append(' OR '.join(o))
        return ' AND '.join(a)

    @staticmethod
    def _parse_endpoint(endpoint='list'):
        if not endpoint or endpoint in ('list', 'show'):
            return ''

        return endpoint if endpoint in ('search', 'filter') else ''

    @staticmethod
    def _parse_url(api, endpoint, params):
        url = '%s/%s/%s' % (Endpoints.host, api, endpoint)

        if not params:
            return url

        keys = map(lambda p: p.lower(), params.keys())

        if endpoint == '' and any(k in ('date', 'id') for k in keys):
            url += params['id'] if 'id' in params else params['date']

        return url

    @staticmethod
    def _parse_params(endpoint, params, filter_keys=None):

        if not params:
            return None

        keys = map(lambda p: p.lower(), params.keys())

        if endpoint == '' and any(k in ('date', 'id') for k in keys):
            return None

        if endpoint in ('filter', 'search') and 'q' not in keys:
            raise ValueError('Expected a query parameter with this endpoint.')

        parsed_params = {}

        for param, value in params.items():
            param = param.lower()

            if param not in ('sort', 'limit', 'skip', 'q'):
                continue

            if endpoint == 'filter' and param == 'q':
                value = Endpoints._process_filter(queries=value,
                                                  filter_keys=filter_keys)

            parsed_params[param] = value

        return parsed_params
