import requests
from .scrape_filters import main as scrape_filters


def get(url, params=None, headers=None):
    return requests.get(url=url, params=params, headers=headers)
