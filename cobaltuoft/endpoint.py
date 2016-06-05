class Endpoint:
    host = 'http://cobalt.qas.im/api/1.0'

    @staticmethod
    def run(api, get, endpoint=None, params=None, filter_keys=None):
        endpoint = Endpoint._parse_endpoint(endpoint)

        url, params = Endpoint._parse_url(api, endpoint, params), \
            Endpoint._parse_params(endpoint, params, filter_keys)

        return get(url=url, params=params)

    @staticmethod
    def _process_filter(queries, filter_keys=None):
        """Form a Cobalt-filter string with the queries list and filter_keys.
        Outer lists are joined by "AND" and inner lists are joined by "OR".
        """

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
        return '' if (not endpoint or
                      endpoint in ('list', 'show') or
                      endpoint not in ('search', 'filter')) else endpoint

    @staticmethod
    def _parse_url(api, endpoint, params):
        url = '%s/%s/%s' % (Endpoint.host, api, endpoint)

        if not params:
            return url

        keys = map(lambda p: p.lower(), params.keys())

        if endpoint == '' and any(k in ('date', 'id') for k in keys):
            url += put_value(params, 'id', params['date'])

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
                value = Endpoint._process_filter(queries=value,
                                                 filter_keys=filter_keys)

            parsed_params[param] = value

        return parsed_params
