import requests
import json
from bs4 import BeautifulSoup

BASE_URL = 'https://cobalt.qas.im/documentation/%s/filter'
ACTIVE_APIS = [
    'athletics',
    'buildings',
    'courses',
    'food',
    'textbooks'
]


def scrape(api):
    host = BASE_URL % api
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


def main():
    filters = {}
    for api in ACTIVE_APIS:
        filters[api] = scrape(api)
    return filters

if __name__ == '__main__':
    main()
