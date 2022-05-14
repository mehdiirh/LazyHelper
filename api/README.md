# LazyHelper API

LazyHelper provides REST API. 

if you have smart home or a central application and need to control your PC from there, you can use these endpoints

## - Authentication :
If authentication is required, you have to pass your `api_key` in headers in all of your requests.

> #### ❓ WHERE IS API KEY?
> 
>you can find your `api_key` in `panel -> Profile` of your LazyHelper.
> If you didn't create a superuser at the first, create one by:
>```shell
> ./manage.py createsuperuser
> ```


Example of headers:
```json
{"Authorization": "123abc456def789ijk0lmno"}
```

## - Endpoints
Here is a list of all API endpoints.

Name                 | Docs
:---                 | :---
Execute commands     | [Docs](endpoints/execute.md)
Get list of commands | [Docs](endpoints/commands.md)