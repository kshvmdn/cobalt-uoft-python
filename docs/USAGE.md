## Usage

### Classes

  - Request
    - [Cobalt](#cobaltuoftcobalt)
    - [Datasets](#cobaltuoftdatasets)
  
  - Response
    - [Response](#cobaltuoftresponseresponse)

### API

#### `cobaltuoft.Cobalt`
  
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
    * The `q` value for `params` can either be a [Cobalt-filter string](https://cobalt.qas.im/documentation/courses/filter) or a nested list of key-value pairs.
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

---

#### `cobaltuoft.Datasets`
  
  - Interface with full [Cobalt datasets](https://github.com/cobalt-uoft/datasets). Data is returned as a [`Response`](#cobaltuoftresponseresponse) object.
  
  - This class doesn't need to be instantiated, instead call it's methods directly.
  
  - `Datasets.run()`

    | Parameter  | Type          | Description
    | ---        | ---           | ---
    | `tag`      | `str`         | The [release tag](https://api.github.com/repos/cobalt-uoft/datasets/tags) to request data for. Defaults to `'latest'`.
    | `datasets` | `str|[str]`   | The [datasets](https://api.github.com/repos/cobalt-uoft/datasets/contents?ref={TAG}) to return. Accepts a list of datasets, `'*'` for all, or a single dataset.

---

#### `cobaltuoft.response.Response`

  - The response object for each of the request modules.

  | Attribute  | Type                 | Description
  | ---        | ---                  | ---
  | `data`     | `dict|[dict]|None`   | The response body.
  | `error`    | `dict|None`          | The error message and status code.
  | `url`      | `str`                | The request URL with query parameters.