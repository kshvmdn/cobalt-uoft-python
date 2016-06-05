import requests
import json

from bs4 import BeautifulSoup

BASE_URL = 'https://cobalt.qas.im'


def main():
    """Scrape the active APIs from the Cobalt homepage."""

    resp = requests.get(BASE_URL)
    soup = BeautifulSoup(resp.text, 'html.parser')

    if not soup.find(id='apis'):
        return []

    return [a.text.lower() for a in soup.find(id='apis').find_all('a')]

if __name__ == '__main__':
    main()
