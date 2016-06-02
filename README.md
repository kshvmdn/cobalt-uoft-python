# cobaltuoft [![PyPI version](https://badge.fury.io/py/cobaltuoft.svg)](https://badge.fury.io/py/cobaltuoft)

A Python wrapper for interfacing with [Cobalt](http://github.com/cobalt-uoft), open data [APIs](http://cobalt.qas.im) and [datasets](http://github.com/cobalt-uoft/datasets) for the University of Toronto.

## Requirements

* Python 3

## Installation

```sh
pip3 install cobaltuoft
```

## Usage

### Classes

* [Cobalt](#cobaltuoftcobalt)
* [Datasets](#cobaltuoftdatasets)

### API

#### `cobaltuoft.Cobalt`

  * Directly interface with [Cobalt](http://cobalt.qas.im) APIs. Data is returned as a native Python object (`[dict]` or `dict`).

  * Initialize the class (a key is required, get one [here](https://cobalt.qas.im/signup)).

    ```py
    >>> from cobaltuoft import Cobalt
    >>> cobalt = Cobalt('API_KEY')
    ```

  * Each [active API](https://cobalt.qas.im/#apis) can be accessed through a method of the same name.

  * Method parameters:

    * `endpoint` –  The endpoint to be accessed for the respective API. Any of the following values are accepted (for most of the APIs at least, refer to the docs for exceptions):

      * `None` (used for [list](https://cobalt.qas.im/documentation/courses/list) and [show](https://cobalt.qas.im/documentation/courses/show))
      * [`search`](https://cobalt.qas.im/documentation/courses/search)
      * [`filter`](https://cobalt.qas.im/documentation/courses/filter)

    * `params` – The URL parameters for this query. Accepts `None` or a `dict` of key-value pairs. Any of the following keys are accepted (read more about these parameters [here](https://cobalt.qas.im/documentation/courses/search)):

      | Parameter     | Endpoints                  | Description                                                                                             |
      |---------------|----------------------------|---------------------------------------------------------------------------------------------------------|
      | `limit`       | All except `show`          | The number of results to return.                                                                        |
      | `skip`        | All except `show`          | The number of results to skip.                                                                          |
      | `sort`        | All except `show`          | The sorting procedure to be used on the returned list.                                                  |
      | `q`           | Only `search` or `filter`  | The string to perform a text search with. For filter queries, refer to [this](#filter-queries).         |
      | `id` / `date` | Only `show`                | The `:id` or `:date` value for the [`show`](https://cobalt.qas.im/documentation/courses/show) endpoint. |

  * Examples:
    * `/courses?skip=10`

      ```python
      >>> cobalt.courses(params={'skip': 10})
      [{...}]
      ```

    * `/buildings/134`

      ```python
      >>> cobalt.buildings(params={'id': 134})
      {...} # not a list!
      ```

    * `/food/search?q="pizza"&limit=2`

      ```python
      >>> cobalt.food(endpoint='search', params={
      ...     'q': '"pizza"',
      ...     'limit': 2
      ... })
      [{...}]
      ```

    * `/textbooks/filter?price:>=500 OR author="Queen"`

      ```python
      >>> cobalt.textbooks(endpoint='filter', params={
      ...     'q': [
      ...         [
      ...             ('price', '>=500'),
      ...             ('author', '"Queen"')
      ...         ]
      ...     ]
      ... })
      [{...}]

      # equivalently
      >>> cobalt.textbooks(endpoint='filter', params={
      ...     'q': 'price:>=500 OR author:"Queen"'
      ... })
      [{...}]
      ```

###### Filter Queries

* The `q` value can either be a [Cobalt-filter string](https://cobalt.qas.im/documentation/courses/filter) or a nested list of key-value pairs.
* Outer lists are joined by `"AND"` and inner lists are joined by `"OR"`. Use a `tuple` for the key-value pair.
* You can use [`Cobalt._process_filter`](https://github.com/kshvmdn/cobalt-uoft-python/blob/master/cobaltuoft/endpoints/__init__.py#L17) to test your filters.
* Examples:

  ```python
  >>> [
  ...     [('instructor', '"D Liu"')],
  ...     [('level', '<=200')]
  ... ]
  'instructor:"D Liu" AND level:<=200'
  ```

  ```python
  >>> [
  ...    [('breadth', '!2'), ('code', '"CSC"')]
  ... ]
  'breadth:!2 OR code:"CSC"'
  ```

  ```python
  >>> [
  ...     [('instructor', '"D Liu"')],
  ...     [('level', '<=200')],
  ...     [('breadth', '!2'), ('code', '"CSC"')]
  ... ]
  'instructor:"D Liu" AND level:<=200 AND breadth:!2 OR code:"CSC"'
  ```

--------------------------------------------------------------------------------

#### `cobaltuoft.Datasets`
  * Interface with full [Cobalt datasets](https://github.com/cobalt-uoft/datasets). Data is returned as a native Python object (`[dict]` or `dict`).
  * This class doesn't need to be instantiated, instead call it's methods directly.
  * `Datasets.run`

    | Parameter  | Type   | Description                                                                                                                                                                                                  |
    |------------|--------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | `tag`      |`str`   | The release tag for which to download data from. Defaults to `'latest'`. For a list of available tags, refer to [this](https://api.github.com/repos/cobalt-uoft/datasets/tags) or run `Datasets._get_tags()` |

    ```python
    >>> from cobaltuoft import Datasets
    >>> Datasets.run('2016-2017')
    [{...}]
    ```

## Contribute

This project is completely open source. Feel free to open an [issue](https://github.com/kshvmdn/cobalt-uoft-python/issues) for questions/requests or submit a [pull request](https://github.com/kshvmdn/cobalt-uoft-python/pulls)!
