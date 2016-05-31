from .endpoint import Endpoint


class Courses:
    path = '%s/%s' % (Endpoint.base_url, 'courses')
    filter_terms = [
        'code',
        'name',
        'description',
        'department',
        'division',
        'prerequisite',
        'exclusion',
        'level',
        'breadth',
        'campus',
        'term',
        'meeting_code',
        'instructor',
        'day',
        'start',
        'end',
        'duration',
        'location',
        'size',
        'enrolment'
    ]

    @staticmethod
    def run(endpoint, params, get):
        endpoint = Endpoint._parse_endpoint(endpoint) or ''
        return get(url=Endpoint._parse_url(Courses.path, endpoint, params),
                   params=Endpoint._parse_params(endpoint, params, Courses.filter_terms))
