## cobaltuoft [![PyPI version](https://badge.fury.io/py/cobaltuoft.svg)](https://badge.fury.io/py/cobaltuoft)

A Python wrapper for interfacing with [Cobalt](http://github.com/cobalt-uoft), open data [APIs](http://cobalt.qas.im) and [datasets](http://github.com/cobalt-uoft/datasets) for the University of Toronto.

### Documentation

- [Getting started](#getting-started)
- [Usage](#usage)
- [Examples](#examples)
- [Contribute](#contribute)

--- 

### Getting started

#### Installation

1. Install through `pip`.

  ```
  pip install cobaltuoft
  ```

2. Install via source (download from [here](https://github.com/kshvmdn/cobalt-uoft-python/archive/master.zip)).

  ```sh
  $ git clone https://github.com/kshvmdn/cobalt-uoft-python.git
  $ cd cobalt-uoft-python && pip install -r ./requirements.txt
  ```

---

### Usage

#### Classes

  - Request objects
    + [Cobalt](#cobaltuoftcobalt)
    + [Datasets](#cobaltuoftdatasets)
  
  - Response objects
    + [Response](#cobaltuoftresponseresponse)

#### API

##### `cobaltuoft.Cobalt`
  
  - Directly interface with [Cobalt](http://cobalt.qas.im) APIs. Data is returned as a [`Response`](#cobaltuoftresponseresponse) object.

  - Initialize the class (a Cobalt API key is required, get one [here](https://cobalt.qas.im/signup)).

    ```py
    >>> from cobaltuoft import Cobalt
    >>> cobalt = Cobalt(api_key='API_KEY')
    ```

  - Each [active API](https://cobalt.qas.im/#apis) can be accessed through a method of the same name. These methods have two optional parameters:

    + `endpoint` –  The endpoint to be accessed for the respective API. Any of the following values are accepted (for most of the APIs, refer to the docs for exceptions):

      - [`list`](https://cobalt.qas.im/documentation/courses/list) (default)
      - [`show`](https://cobalt.qas.im/documentation/courses/show)
      - [`search`](https://cobalt.qas.im/documentation/courses/search)
      - [`filter`](https://cobalt.qas.im/documentation/courses/filter)

    + `params` – The URL parameters for this query. Accepts a `dict` of key-value pairs. Any of the following keys are accepted (read more about these parameters [here](https://cobalt.qas.im/documentation/courses/search)):

      | Parameter   | Endpoints            | Description
      | ---         | ---                  | ---
      | `limit`     | All except `show`    | The number of results to return.
      | `skip`      | All except `show`    | The number of results to skip.
      | `sort`      | All except `show`    | The sorting procedure to be used on the returned list.
      | `q`         | `search` or `filter` | The search or filter query. For filter queries, refer to [this](#filter-queries).
      | `id`/`date` | `show`               | The `:id` or `:date` value.

  - <a name="filter-queries"/>Filter Queries</a>
    * When using `filter`, the `q` parameter can either be a [Cobalt-filter string](https://cobalt.qas.im/documentation/courses/filter) or a nested list of key-value pairs.
    * Outer lists are joined by `"AND"` and inner lists are joined by `"OR"`. Use a `tuple` for the key-value pair.
    * You can use [`Cobalt._process_filter`](cobaltuoft/endpoints/__init__.py#L14) to test your filters.
    * Here are some examples:

      - `'instructor:"D Liu" AND level:<=200'`

        ```python
        >>> [
        ...     [('instructor', '"D Liu"')],
        ...     [('level', '<=200')]
        ... ]
        ```

      - `'breadth:!2 OR code:"CSC"'`

        ```python
        >>> [
        ...    [('breadth', '!2'), ('code', '"CSC"')]
        ... ]
        ```

      - `instructor:"D Liu" AND level:<=200 AND 'breadth:!2 OR code:"CSC"'`

        ```python
        >>> [
        ...     [('instructor', '"D Liu"')],
        ...     [('level', '<=200')],
        ...     [('breadth', '!2'), ('code', '"CSC"')]
        ... ]
        ```

##### `cobaltuoft.Datasets`
  
  - Interface with full [Cobalt datasets](https://github.com/cobalt-uoft/datasets). Data is returned as a [`Response`](#cobaltuoftresponseresponse) object.
  
  - This class doesn't need to be instantiated, instead call it's methods directly.
  
  - `Datasets.run()`

    | Parameter  | Type          | Description
    | ---        | ---           | ---
    | `tag`      | `str`         | The [release tag](https://api.github.com/repos/cobalt-uoft/datasets/tags) to request data for. Defaults to `'latest'`.
    | `datasets` | `str|[str]`   | The [datasets](https://api.github.com/repos/cobalt-uoft/datasets/contents?ref={TAG}) to return. Accepts a list of datasets, `'*'` for all, or a single dataset.
  
  - [Examples](./examples)

##### `cobaltuoft.response.Response`

  - The response object for each of the request modules.

  | Attribute  | Type                 | Description
  | ---        | ---                  | ---
  | `data`     | `dict|[dict]|None`   | The response body.
  | `error`    | `dict|None`          | The error message and status code.
  | `url`      | `str`                | The request URL with query parameters.

---

### Examples

- More detailed examples can be found [here](./examples).

#### `cobaltuoft.Cobalt`

```py
from cobaltuoft import Cobalt
cobalt = Cobalt(api_key='API_KEY')
```

```py
>>> courses = cobalt.courses(params={'skip': 10})
>>> courses
<class 'cobaltuoft.response.Response'>
>>> courses.error
None
>>> courses.data
[..., {...}]
>>> courses.url
'http://cobalt.qas.im/api/1.0/courses?skip=10&key={KEY}'
```

```py
>>> building_134 = cobalt.buildings(endpoint='search', params={'id': 134})
>>> building_134.error
None
>>> building_134.data
{...} # not a list!
>>> building_134.url
'http://cobalt.qas.im/api/1.0/buildings/134?key={KEY}'
>>> building_1738 = cobalt.buildings(endpoint='search', params={'id': 1738})
>>> building_1738.error
{
    'status_code': 400, 
    'message': 'A building with the specified identifier does not exist.'
}
>>> building_1738.data
None
>>> building_1738.url
'http://cobalt.qas.im/api/1.0/buildings/1738?key={KEY}'
```

```py
>>> food = cobalt.food(endpoint='search', params={
...     'q': '"pizza"',
...     'limit': 2
... })
>>> food.error
None
>>> food.data
[{...}, {...}]
>>> food.url
'http://cobalt.qas.im/api/1.0/food/search?q="pizza"&limit=2&key={KEY}'
```

```py
>>> textbooks = cobalt.textbooks(endpoint='filter', params={
...     'q': [
...         [
...             ('price', '>=500'),
...             ('author', '"Queen"')
...         ]
...     ] # equivalent to 'q': 'price:>=500 OR author:"Queen"'
... })
>>> textbooks.error
None
>>> textbooks.data
[..., {...}]
>>> textbooks.url
'http://cobalt.qas.im/api/1.0/textbooks/filter?q=price:>=500 OR author="Queen"&key={KEY}'
```

--- 

#### `cobaltuoft.Datasets`

```py
from cobaltuoft import Datasets
```

```py
>>> latest_datasets = Datasets.run(tag='latest', datasets='*')
>>> latest_datasets.error
None # the GitHub API only allows 60 requests per hour, this will be non-None after you hit that limit.
>>> latest_datasets.data
{
    ...,
    'courses': [..., {...}], 
    'athletics': [..., {...}]
} 
```

```py
>>> courses_2015 = Datasets.run(tag='2015-2016', datasets='courses')
>>> courses_2015.data
{
    'courses': [..., {...}]
}
>>> courses_2015.url
None # Datasets responses don't have a `url` attribute!
```

```py
>>> datasets = Datasets.run(datasets=['athletics', 'shuttles', 'parking', 'libraries'])
>>> import json
>>> with open('datasets.json', 'w') as f:
...     f.write(json.dumps(datasets.data, indent=2))
# https://gist.github.com/kshvmdn/6103bab0ff86fbc904b27c8072a32a2b
```


--- 

### Contribute

This project is completely open source. Feel free to open an [issue](https://github.com/kshvmdn/cobalt-uoft-python/issues) for questions/requests or submit a [pull request](https://github.com/kshvmdn/cobalt-uoft-python/pulls).

#### Development

- Clone the project.

  ```sh
  git clone https://github.com/kshvmdn/cobalt-uoft-python.git && cd cobalt-uoft-python
  ```

- Install requirements.

  ```sh
  pip install -r ./requirements.txt
  ```
