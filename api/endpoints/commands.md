## Get list of commands

```
POST /api/commands/
```


You can filter the response by passing queries in data, using these search fields:

Key             | Type   | Description 
:---            | :---:  | :---
active          | bool   | only returns active commands 
buttons__active | bool   | only returns commands which have active buttons

For example: 
If you want to get only custom-commands which have a button you can do:

```json
{"active": true, "buttons__active": true}
```

A working example in python:
```python
import requests

headers = {
    'authorization': '123abc456def789ijk0lmno'
}

data = {
    "active": True
}

response = requests.post(
    'http://localhost:8081/api/commands/',
    headers=headers,
    data=data
)

print(response.json())
```

Example response:
```json
{
  "data": {
    "6": {
      "title": "List of files",
      "command": "ls",
      "short_code": "list-of-files",
      "description": "Show a list of files in current directory",
      "active": true,
      "has_buttons": true,
      "buttons": {
        "10": {
          "color": "#FFC312",
          "active": true
        }
      }
    }
  },
  "meta": {
    "status": "ok",
    "code": 200
  }
}
```