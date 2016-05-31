import requests
import json
from bs4 import BeautifulSoup

BASE_URL = 'https://cobalt.qas.im/documentation/%s/filter'
ACTIVE_APIS = ['buildings', 'courses']


def scrape(api):
    host = BASE_URL % api
    resp = requests.get(host)
    soup = BeautifulSoup(resp.text, 'html.parser')

    return [tr.find('td').text
            for tr in soup.find('table').find_all('tr')[1:]]


def main():
    filters = {}
    for api in ACTIVE_APIS:
        filters[api] = scrape(api)
    return filters

if __name__ == '__main__':
    main()
