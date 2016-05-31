import requests
import json
from bs4 import BeautifulSoup

base = 'https://cobalt.qas.im/documentation/{}/filter'


def scrape(api):
    filters = []

    host = base.format(api)
    resp = requests.get(host)
    soup = BeautifulSoup(resp.text, 'html.parser')

    for tr in soup.find('table').find_all('tr')[1:]:
        filters.append(tr.find('td').text)

    return filters

if __name__ == '__main__':
    filters = {}
    for api in ('buildings', 'courses'):
        filters[api] = scrape(api)

    with open('filter_mapping.json', 'w+') as f:
        f.write(json.dumps(filters, indent=2))
