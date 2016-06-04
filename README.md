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

- Directly interface with [Cobalt](http://cobalt.qas.im) APIs. Data is returned as a native Python object.

- Initialize the class (an API key is required, get one [here](https://cobalt.qas.im/signup)).
  
  ```py
  >>> from cobaltuoft import Cobalt
  >>> cobalt = Cobalt('API_KEY')
  ```

- Each [active API](https://cobalt.qas.im/#apis) can be accessed through a method of the same name. See examples [below](#api-method-examples). These methods have two optional parameters.

  - `endpoint` –  The endpoint to be accessed for the respective API. Any of the following values are accepted (for most of the APIs at least, refer to the docs for exceptions):
    
    - [`list`](https://cobalt.qas.im/documentation/courses/list) (default)
    - [`show`](https://cobalt.qas.im/documentation/courses/show)
    - [`search`](https://cobalt.qas.im/documentation/courses/search)
    - [`filter`](https://cobalt.qas.im/documentation/courses/filter)

  - `params` – The URL parameters for this query. Accepts `None` or a `dict` of key-value pairs. Any of the following keys are accepted (read more about these parameters [here](https://cobalt.qas.im/documentation/courses/search)):

    | Parameter   | Endpoints            | Description
    | ---         | ---                  | ---
    | `limit`     | All except `show`    | The number of results to return.
    | `skip`      | All except `show`    | The number of results to skip.
    | `sort`      | All except `show`    | The sorting procedure to be used on the returned list.
    | `q`         | `search` or `filter` | The search or filter string. For filter queries, refer to [this](#filter-queries).  
    | `id`/`date` | `show`               | The `:id` or `:date` value.

- <a name="filter-queries"/>Filter Queries</a>
  - The `q` value for `params` can either be a [Cobalt-filter string](https://cobalt.qas.im/documentation/courses/filter) or a nested list of key-value pairs.
  - Outer lists are joined by `"AND"` and inner lists are joined by `"OR"`. Use a `tuple` for the key-value pair.
  - You can use [`Cobalt._process_filter`](cobaltuoft/endpoints/__init__.py#L14) to test your filters.
  
    > `'instructor:"D Liu" AND level:<=200'`

    ```python
    >>> [
    ...     [('instructor', '"D Liu"')],
    ...     [('level', '<=200')]
    ... ]
    ```
  
    > `'breadth:!2 OR code:"CSC"'`

    ```python
    >>> [
    ...    [('breadth', '!2'), ('code', '"CSC"')]
    ... ]
    ```
    
    > `instructor:"D Liu" AND level:<=200 AND 'breadth:!2 OR code:"CSC"'`
    
    ```python
    >>> [
    ...     [('instructor', '"D Liu"')],
    ...     [('level', '<=200')],
    ...     [('breadth', '!2'), ('code', '"CSC"')]
    ... ]
    ```

- <a name="api-method-examples"/>Examples</a>
   
  > `/courses?skip=10`

  ```python
  >>> cobalt.courses(params={'skip': 10})
  [{...}]
  ```

  > `/buildings/134`

  ```python
  >>> cobalt.buildings(params={'id': 134})
  {...}
  ```

  > `/food/search?q="pizza"&limit=2`
    
  ```python
  >>> cobalt.food(endpoint='search', params={
  ...     'q': '"pizza"',
  ...     'limit': 2
  ... })
  [{...}]
  ```
  
  > `/textbooks/filter?price:>=500 OR author="Queen"`

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

---

#### `cobaltuoft.Datasets`
  * Interface with full [Cobalt datasets](https://github.com/cobalt-uoft/datasets). Data is returned as a native Python object.
  * This class doesn't need to be instantiated, instead call it's methods directly.
  * `Datasets.run`

    | Parameter  | Type       | Description
    | ---        | ---        | ---
    | `tag`      |`str`       | The [release tag](https://api.github.com/repos/cobalt-uoft/datasets/tags) to obtain data from. Defaults to `'latest'`.
    | `datasets` |`str|[str]` | The [datasets](https://api.github.com/repos/cobalt-uoft/datasets/contents?ref={TAG}) to return. Accepts a list for multiple sets, `'*'` for all (default) or a single string.

    ```python
    >>> from cobaltuoft import Datasets
    >>> Datasets.run(tag='2016-2017')
    {...}
    >>> Datasets.run(datasets=['courses', 'athletics'])
    {
        'courses': [{...}],
        'buildings': [{...}]
    }
    ```

## Contribute

This project is completely open source. Feel free to open an [issue](https://github.com/kshvmdn/cobalt-uoft-python/issues) for questions/requests or submit a [pull request](https://github.com/kshvmdn/cobalt-uoft-python/pulls)!
