import requests
import json

from bs4 import BeautifulSoup

BASE_URL = 'https://cobalt.qas.im/documentation/%s/filter'


def scrape(api_endpoint):
    """Scrape filter keys from the Cobalt documentation of api_endpoint."""

    host = BASE_URL % api_endpoint
    resp = requests.get(host)
    soup = BeautifulSoup(resp.text, 'html.parser')

    filters = []

    if not soup.find('table'):
        return filters

    for tr in soup.find('table').find_all('tr'):
        if tr.find('th') or not tr.find('td'):
            continue

        filters.append(tr.find('td').text)

    return filters


def main(active_apis):
    """Scrape and return filter keys for active_apis."""
    filters = {}
    for api in active_apis:
        filters[api] = scrape(api)
    return filters

if __name__ == '__main__':
    main()
