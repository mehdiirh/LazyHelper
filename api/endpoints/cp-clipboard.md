## Execute commands

> ### 📦 To use this feature, you need to install [xclip](https://github.com/astrand/xclip)


```shell
POST /api/copy/
```


You have to pass your `content` in request data.

Example of data:
```json
{"content": "Copy Me !"}
```

A working example in python:
```python
import requests

headers = {
    'authorization': '123abc456def789ijk0lmno'
}

data = {
    'content': 'Copy Me !'
}

response = requests.post(
    'http://localhost:8081/api/copy/',
    headers=headers,
    data=data
)

print(response.json())
```

Example response:
```json
{
  "data": {
    "content": "Copy Me!"
  },
  "meta": {
    "status": "ok",
    "code": 200
  }
}
```