from collections import OrderedDict


class Endpoint:
    """An superclass for API endpoints."""

    base_url = 'http://cobalt.qas.im/api/1.0'

    @staticmethod
    def _process_filter(queries, map):
        # [[(), (), ()], [(), (), ()], [()]]

        if (type(queries) == str):
            return queries

        a = []
        for filter in queries:
            o = []
            for k, v in filter:
                if k.lower() not in map:
                    continue
                o.append('%s:%s' % (k, v))
            a.append(' OR '.join(o))
        return ' AND '.join(a)

    @staticmethod
    def _parse_endpoint(endpoint):
        if not endpoint:
            return None

        endpoint = endpoint.lower().strip().replace('/', '')

        if endpoint in ('search', 'filter'):
            return endpoint

        return None

    @staticmethod
    def _parse_params(endpoint, params, map):
        if not params:
            return None

        parsed_params = OrderedDict()

        for param, value in params.items():
            param = param.lower()

            if param not in ('sort', 'limit', 'skip', 'q'):
                continue

            if 'filter' in endpoint and param == 'q':
                value = Endpoint._process_filter(value, map)

            if param not in parsed_params:
                parsed_params[param] = ''

            parsed_params[param] += value

        return dict(parsed_params)

    @staticmethod
    def _parse_url(base_path, endpoint, params):
        url = '%s/%s/' % (base_path, endpoint)

        if endpoint == '' and ('date' in params or 'id' in params):
            url += params['id'] if 'id' in params else params['date']

        return url
