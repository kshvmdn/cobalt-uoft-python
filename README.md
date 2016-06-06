# cobaltuoft [![PyPI version](https://badge.fury.io/py/cobaltuoft.svg)](https://badge.fury.io/py/cobaltuoft)

A Python wrapper for interfacing with [Cobalt](http://github.com/cobalt-uoft), open data [APIs](http://cobalt.qas.im) and [datasets](http://github.com/cobalt-uoft/datasets) for the University of Toronto.

## Getting started

```py
>>> from cobaltuoft import Cobalt, Datasets
```


```py
>>> cobalt = Cobalt(api_key='API_KEY')
>>> courses = cobalt.courses()
>>> cs_courses = cobalt.courses(endpoint='search', params={
...     'q': 'computer science'
... })
```

```py
>>> datasets = Datasets.run()
>>> courses_dataset_2015 = Datasets.run(tag='2015-2016', datasets='courses')
```

Checkout the full [documentation](docs) for a detailed guide and [examples](docs/EXAMPLE.md).

## Contribute

This project is completely open source. Feel free to open an [issue](https://github.com/kshvmdn/cobalt-uoft-python/issues) for questions/requests or submit a [pull request](https://github.com/kshvmdn/cobalt-uoft-python/pulls).

Read more about contributing [here](docs/CONTRIBUTE.md).
