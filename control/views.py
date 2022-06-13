import requests
from django.contrib.auth import logout as logout_user, authenticate as auth_user, login as login_user
from django.http.response import JsonResponse
from django.shortcuts import render, reverse, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from config.models import Button, Config
from utils.api.tools import get_request_data, api_response
from utils.core.tools import linux_package_installed
from utils.core import http_status as sc


@ensure_csrf_cookie
def control(request):

    custom_buttons = Button.objects.filter(active=True, command__active=True).all()

    context = {
        'custom_buttons': custom_buttons,
        'xclip': linux_package_installed('xclip'),
        'user': request.user,
    }

    return render(request, 'index.html', context=context)


@require_POST
def initial_data(request):

    data = dict()
    login_required = Config.objects.get(key='login-required').active

    data['settings'] = {setting.key: setting.active for setting in Config.objects.all()}

    data['user'] = {
        'is_logged_in': request.user.is_authenticated,
        'is_admin': request.user.is_superuser,
        'user': request.user.username,
    }

    if request.user.is_superuser:
        data['links'] = {
                'logout': reverse('logout'),
                'panel': reverse('admin:index'),
                'settings': reverse('admin:config_config_changelist')
            }
    else:
        data['links'] = {
            'login': reverse('ajax-login')
        }

    if not login_required or request.user.is_superuser:
        buttons = Button.objects.filter(active=True, command__active=True).all()

        data['custom_buttons'] = [
            {
                'id': button.id,
                'title': button.command.title,
                'short_code': button.command.short_code,
                'color': button.color
            }
            for button in buttons
        ]

        data['links']['add_buttons'] = reverse('admin:config_button_add')

    return api_response(
        request,
        data=data,
    )


@require_POST
def ajax_exec(request):
    api_key = None
    if request.user.is_staff:
        api_key = request.user.profile.api_key

    data = get_request_data(request)
    command = data.get('command')

    # build absolute uri for "command execution" API endpoint and
    # send command to it
    execute_command_endpoint = request.build_absolute_uri(reverse('exec-command'))
    response = requests.post(
        execute_command_endpoint,
        headers={'authorization': api_key},  # send user api_key ( if authenticated )
        data={'command': str(command)}
    )

    return JsonResponse(response.json(), status=sc.HTTP_200_OK)


@require_POST
def ajax_copy_to_clipboard(request):
    api_key = None
    if request.user.is_staff:
        api_key = request.user.profile.api_key

    data = get_request_data(request)
    content = data.get('content')

    # build absolute uri for "copy to clipboard" API endpoint and
    # send content to it
    copy_to_clipboard_endpoint = request.build_absolute_uri(reverse('copy-to-clipboard'))
    response = requests.post(
        copy_to_clipboard_endpoint,
        headers={'authorization': api_key},  # send user api_key ( if authenticated )
        data={'content': str(content)}
    )

    return JsonResponse(response.json(), status=sc.HTTP_200_OK)


@require_POST
def login(request):
    data = get_request_data(request)
    username = data.get('username')
    password = data.get('password')

    user = auth_user(request, username=username, password=password)
    if user is not None:
        login_user(request, user)
        response = api_response(request, {'success': True}, status=True, return_json=True)
    else:
        response = api_response(request, status=False, status_code=sc.HTTP_403_FORBIDDEN, return_json=True)

    return JsonResponse(response, status=sc.HTTP_200_OK)


def logout(request):
    logout_user(request)
    return redirect('control')
