# cobaltuoft

[![PyPI version](https://badge.fury.io/py/cobaltuoft.svg)](https://badge.fury.io/py/cobaltuoft)

A Python library for interfacing with publicly available UofT open data through [Cobalt](http://cobalt.qas.im).

## Requirements

* Python 3

## Installation

`pip3 install cobaltuoft`

## Usage

### Classes

* [Cobalt](#cobaltuoftcobalt)
* [Datasets](#cobaltuoftdatasets)

### API

#### `cobaltuoft.Cobalt`

Directly interface with [Cobalt](http://cobalt.qas.im) APIs. Data is returned as a native Python dictionary.
  
  * Initialize the class, a key is required to use this class (get yours [here](https://cobalt.qas.im/signup)).

    ```python
    from cobaltuoft import Cobalt
    cobalt = Cobalt('API_KEY')
    ```

  * Each [active API](https://cobalt.qas.im/#apis) can be accessed through a method of the same name.
  
  * Method parameters:
    
    * `endpoint` –  The endpoint to be accessed for the respective API. One of `None` (used for [list](https://cobalt.qas.im/documentation/courses/list) and [show](https://cobalt.qas.im/documentation/courses/show)), [`search`](https://cobalt.qas.im/documentation/courses/search), or [`filter`](https://cobalt.qas.im/documentation/courses/filter).
    
    * `params` – The URL parameters for this query. Possible parameter keys (read more about these parameters in the [Cobalt docs](https://cobalt.qas.im/documentation/courses/search)):
    
      | Parameter     | Endpoints                  | Description                                                                                                      |
      |---------------|----------------------------|------------------------------------------------------------------------------------------------------------------|
      | `limit`       | All (except `show`)        | The number of results to return.                                                                                 |
      | `skip`        | All (except `show`)        | The number of results to skip.                                                                                   |
      | `sort`        | All (except `show`)        | The sorting procedure to be used on the returned list.                                                           |
      | `q`           | Only `search` or `filter`  | The string to perform a text search with. For filter queries, refer to [this](#filter-queries).                  |
      | `id` / `date` | Only `show`                | The `:id` or `:date` endpoint value for the [`show`](https://cobalt.qas.im/documentation/courses/show) endpoint. |

  * Examples:
    * `/courses?skip=10`
    
      ```python
      courses = cobalt.courses(params={'skip': 10})
      ```
    
    * `/buildings/134`
    
      ```python
      buildings = cobalt.courses(params={'id': 134})
      ```
   
    * `/food/search?q="pizza"&limit=2`
    
      ```python
      food = cobalt.food(endpoint='search', params={
          'q': '"pizza"',
          'limit': 2
      })
      ```
   
    * `/textbooks/filter?price:>=500 OR author="Queen"`
      
      ```python
      textbooks = cobalt.textbooks(endpoint='filter', params={
          'q': [
              [
                  ('price', '>=500'),
                  ('author', '"Queen"')
              ]
          ]
      })

      # equivalently:
      textbooks = cobalt.textbooks(endpoint='filter', params={
          'q': 'price:>=500 OR author:"Queen"'
      })
      ```

###### Filter Queries

* Parameter value for `q` can be passed as a [Cobalt-filter string](https://cobalt.qas.im/documentation/courses/filter) or a nested list of key-value pairs.
* Outer lists are joined by `"AND"` and inner lists are joined by `"OR"`.
* Use a tuple for the key-value pair.
* Examples:

  * `instructor:"D Liu" AND level:<=200`
  
    ```python
    [
        [('instructor', '"D Liu"')], 
        [('level', '<=200')]
    ]
    ```
  
  * `breadth:!2 OR code:"CSC"`
  
    ```python
    [
        [('breadth', '!2'), ('code', '"CSC"')]
    ]
    ```
  
  * `instructor:"D Liu" AND level:<=200 AND level:<=200 AND breadth:!2 OR code:"CSC"`
  
    ```python
    [
        [('instructor', '"D Liu"')], 
        [('level', '<=200')],
        [('breadth', '!2'), ('code', '"CSC"')]
    ]
    ```

--------------------------------------------------------------------------------

#### `cobaltuoft.Datasets`

  * Interface with full [Cobalt datasets](https://github.com/cobalt-uoft/datasets). Data is returned as a native Python dictionary.
  * This class doesn't need to be instantiated, instead call it's methods directly.
  * Currently only has a single method, `run`, parameters:

    | Name     | Value | Description                                                                                                                                                                                                  |
    |----------|-------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | `tag`    | `str` | The release tag for which to download data from. Defaults to `'latest'`. For a list of available tags, refer to [this](https://api.github.com/repos/cobalt-uoft/datasets/tags) or run `Datasets._get_tags()` |

  ```python
  from cobaltuoft import Datasets

  datasets = Datasets.run()
  ```

## Contribute

This project is completely open source. Feel free to open an [issue](https://github.com/kshvmdn/cobalt-uoft-python/issues) for questions/requests or submit a [pull request](https://github.com/kshvmdn/cobalt-uoft-python/pulls)
