## Examples

#### `cobaltuoft.Cobalt`

```py
from cobaltuoft import Cobalt
cobalt = Cobalt(api_key='API_KEY')
```

- `/courses?skip=10`

  ```python
  >>> courses = cobalt.courses(params={'skip': 10})
  >>> courses.error
  None
  >>> courses.data
  [..., {...}]
  ```

- `/buildings/134`

  ```python
  >>> building_134 = cobalt.buildings(endpoint='search', params={
  ...     'id': 134
  ... })
  >>> building_134.data
  {...} # not a list!
  >>> building_999999 = cobalt.buildings(endpoint='search', params={
  ...     'id': 999999
  ... })
  >>> building_999999.url
  'http://cobalt.qas.im/api/1.0/buildings/999999?key={KEY}'
  >>> building_999999.error
  {
      'status_code': 400, 
      'message': 'A building with the specified identifier does not exist.'
  }
  ```

- `/food/search?q="pizza"&limit=2`

  ```python
  >>> food = cobalt.food(endpoint='search', params={
  ...     'q': '"pizza"',
  ...     'limit': 2
  ... })
  >>> food.data
  [{...}, {...}]
  ```

- `/textbooks/filter?price:>=500 OR author="Queen"`

  ```python
  >>> textbooks = cobalt.textbooks(endpoint='filter', params={
  ...     'q': [
  ...         [
  ...             ('price', '>=500'),
  ...             ('author', '"Queen"')
  ...         ]
  ...     ]
  ... })
  >>> textbooks
  <class 'cobaltuoft.response.Response'>
  >>> textbooks.url
  'http://cobalt.qas.im/api/1.0/textbooks/filter?q=price:>=500 OR author="Queen"&key={KEY}'
  >>> textbooks_2 = cobalt.textbooks(endpoint='filter', params={
  ...     'q': 'price:>=500 OR author:"Queen"'
  ... })
  >>> textbooks_2.url
  'http://cobalt.qas.im/api/1.0/textbooks/filter?q=price:>=500 OR author="Queen"&key={KEY}'
  ```

--- 

#### `cobaltuoft.Datasets`

```py
from cobaltuoft import Datasets
```

```py
>>> latest_datasets = Datasets.run(tag='latest', datasets='*')
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
