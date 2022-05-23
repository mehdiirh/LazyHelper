from django.http.response import JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from django.core.handlers.wsgi import QueryDict
from django.contrib.auth.models import User

from api.models import ReceivedRequest
from config.models import Config

from utils.core import http_status as sc
from utils.core.exceptions import AuthenticationError

from typing import Union
import json


def get_client_ip(request: WSGIRequest) -> str:
    """
    get client ip from request

    Args:
        request (WSGIRequest): WSGIRequest

    Returns:
        str: user ip address
    """

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', None)
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def get_request_headers(request: WSGIRequest) -> dict:
    """
    get `request` headers

    Args:
        request (WSGIRequest): WSGIRequest

    Returns:
        dict: a dictionary of headers
    """

    headers = request.headers

    keys = tuple(map(lambda x: x.lower(), headers.keys()))
    values = tuple(headers.values())

    return dict(zip(keys, values))


def get_request_data(request: WSGIRequest):
    """
    get `request` data based on request method, or request body if method-data is not present

    Args:
        request (WSGIRequest): WSGIRequest

    Returns:
        dict: a dictionary of data
    """

    data = {}
    _data = request.__getattribute__(request.method)  # GET, POST, SET, PUT, DELETE

    if not _data:
        _data = request.body

    if not _data:
        return data

    if isinstance(_data, QueryDict):
        for key in _data.keys():
            value = _data.getlist(key)

            if len(value) == 1:
                value = value[0]
            data[key.lower()] = value

    elif isinstance(_data, bytes):
        try:
            data = json.loads(_data)
        except json.decoder.JSONDecodeError:
            pass

    return data


def get_search_query(search_fields: list, query_dict: dict) -> dict:
    """
    Create a query-dict based on search fields
    Args:
        search_fields: a list of possible keys to search
        query_dict: query dict for searching

    Returns:
        dict: a query-dict to search
    """

    return dict(filter(
        lambda x: x[0] in search_fields, query_dict.items()
    ))


def api_response(request, data=None, status=True, status_code=sc.HTTP_200_OK,
                 message='', return_json=False, commit=False,
                 private_data=None, **extra_data) -> Union[JsonResponse, dict]:
    """
    make an api response with base response, containing data and meta

    Args:
        return_json: return raw json instead of JsonResponse
        request: request
        data: dictionary of data
        status: status
        status_code: response code
        message: message
        commit: if True, request and response will be saved in DB
        private_data (object): this parameter will be saved in DB, but it won't be visible to the user

    Returns:
        dict or JsonResponse

    """

    if not status and sc.is_success(status_code):
        status_code = sc.HTTP_400_BAD_REQUEST

    if data is None and sc.is_success(status_code):
        status_code = sc.HTTP_404_NOT_FOUND

    if sc.is_client_error(status_code) or sc.is_server_error(status_code):
        status = False

    status = 'ok' if status else 'fail'

    _base = {
        'data': data,
        'meta': {
            'status': status,
            'code': status_code,
        }
    }

    if message:
        _base['meta']['message'] = message

    if extra_data:
        _base['extra'] = extra_data

    if commit:
        save_received_request(request=request, response=_base, private_data=private_data, status_code=status_code)

    if return_json:
        return _base

    return JsonResponse(data=_base, status=status_code)


def save_received_request(request: WSGIRequest, response: dict = None,
                          private_data=None, status_code=None) -> ReceivedRequest:
    """
    Save received api requests and it's response to database

    Args:
        request (WSGIRequest): request object
        response (dict): response of request
        status_code (int): response status code
        private_data (object): this parameter will be saved in DB, but won't be visible to the user

    Returns:
        ReceivedRequest: ReceivedRequest instance
    """

    # get request data
    data = get_request_data(request)

    # mask sensitive data
    headers = get_request_headers(request)

    authorization = headers.get('authorization', None)
    user = None

    if authorization:
        headers['authorization'] = f'{authorization[:3]}***************{authorization[-3:]}'
        user = User.objects.filter(profile__api_key__exact=authorization).first()

    message = None
    if response.get('meta'):
        message = response['meta'].get('message', None)

    command = None
    if data:
        command = data.get('command', None)

    instance = ReceivedRequest.objects.create(
        user=user,
        path=request.path,
        method=request.method,
        client_ip=get_client_ip(request),
        headers=headers,
        data=data,
        command=command,
        response=response,
        private_data=private_data,
        status_code=status_code,
        message=message
    )

    return instance


def user_security_check(request):
    """
    Check user api_key to validate authorization

    Args:
        request (WSGIRequest): request object

    Returns:
         User

    Raise:
        AuthenticationError: if api_key is not valid
    """

    if not Config.objects.get(key__exact='login-required').active:
        return True

    if request.user.is_authenticated:
        if request.user.is_staff:
            return True

    headers = get_request_headers(request)
    api_key = headers.get('authorization', None)

    if not api_key:
        raise AuthenticationError()

    # find user object based on api_key
    try:
        User.objects.get(profile__api_key__exact=api_key)
    except User.DoesNotExist:  # if User does not exist
        raise AuthenticationError()

    return True
