## Execute commands

```shell
POST /api/execute/
```


You have to pass your `command` in request data.

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
```

Example response:
```json
{
  "data": {
    "command": "whoami",
    "output": "root\n"
  },
  "meta": {
    "status": "ok",
    "code": 200
  }
}
```