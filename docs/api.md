#LazyHelper API

LazyHelper provides REST API. 

if you have smart home or a central application and need to control your PC from there, you can use these endpoints

## Execute commands

```shell
POST /api/execute/
```

You have to pass your `api_key` in headers.

> #### ❓ WHERE IS API KEY?
> 
>you can find your `api_key` in `panel -> Profile` of your LazyHelper.
> If you didn't create a superuser at the first, create one by:
>```shell
> ./manage.py createsuperuser
> ```


Example of headers:
```json
{"authorization": "123abc456def789ijk0lmno"}
```

Also, you have to pass your `command` in request data.

Example of data:
```json
{"command": "ls -la"}
```

A working example in python:
```python
import requests

headers = {
    'authorization': '123abc456def789ijk0lmno'
}

data = {
    'command': 'whoami'
}

response = requests.post(
    'http://localhost:8081/api/execute/',
    headers=headers,
    data=data
)

print(response.json())

# response:

# {
#   "data": {
#     "command": "whoami",
#     "output": "root\n"
#   },
#   "meta": {
#     "status": "ok",
#     "code": 200
#   }
# }

```
