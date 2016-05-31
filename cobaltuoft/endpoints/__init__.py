from collections import OrderedDict


class Endpoints:
    host = 'http://cobalt.qas.im/api/1.0'

    @staticmethod
    def run(api, get, endpoint=None, params=None, map=None):
        endpoint = Endpoints._parse_endpoint(endpoint)

        url, params = Endpoints._parse_url(api, endpoint, params), \
            Endpoints._parse_params(endpoint, params, map)

        return get(url=url, params=params)

    @staticmethod
    def _process_filter(queries, map=None):
        # [[(), (), ()], [(), (), ()], [()]])

        if (type(queries) == str):
            return queries

        a = []
        for filter in queries:
            o = []
            for k, v in filter:
                if map and k.lower() not in map:
                    continue
                o.append('%s:%s' % (k, v))
            a.append(' OR '.join(o))
        return ' AND '.join(a)

    @staticmethod
    def _parse_endpoint(endpoint):
        if not endpoint:
            endpoint = ''

        endpoint = endpoint.lower().strip().replace('/', '')
        return endpoint if endpoint in ('search', 'filter') else ''

    @staticmethod
    def _parse_url(api, endpoint, params):
        url = '%s/%s/%s' % (Endpoints.host, api, endpoint)

        if endpoint == '' and ('date' in params or 'id' in params):
            url += params['id'] if 'id' in params else params['date']

        return url

    @staticmethod
    def _parse_params(endpoint, params, map=None):
        if not params:
            return None

        parsed_params = OrderedDict()

        for param, value in params.items():
            param = param.lower()

            if param in ('date', 'id'):
                return None

            if param not in ('sort', 'limit', 'skip', 'q'):
                continue

            if map and endpoint == 'filter' and param == 'q':
                value = Endpoints._process_filter(value, map)

            parsed_params[param] = value

        return dict(parsed_params)
