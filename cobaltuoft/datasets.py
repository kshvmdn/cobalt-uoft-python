from .helpers import get


class Datasets:
    @staticmethod
    def _get(url, params=None, headers=None):
        return get(url=url, params=params, headers=headers)

    def _get_available_datasets(release='latest'):
        pass

    def run():
        pass
