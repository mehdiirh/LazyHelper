import requests

from django.contrib.auth import logout as logout_user
from django.http.response import JsonResponse
from django.shortcuts import render, reverse, redirect
from django.views.decorators.http import require_POST

from utils.core.tools import linux_package_installed
from utils.auth.http.decorators import login_required


@login_required(redirect_login=True, next_redirect='control')
def control(request):

    context = {
        'xclip': linux_package_installed('xclip'),
        'user': request.user,
    }

    return render(request, 'control/main.html', context=context)


@require_POST
def ajax_exec(request):
    api_key = None
    if request.user.is_staff:
        api_key = request.user.profile.api_key

    command = request.POST.get('command')

    # build absolute uri for "command execution" API endpoint and
    # send command to it
    execute_command_endpoint = request.build_absolute_uri(reverse('exec-command'))
    response = requests.post(
        execute_command_endpoint,
        headers={'authorization': api_key},  # send user api_key ( if authenticated )
        data={'command': str(command)}
    )

    return JsonResponse(response.json(), status=200)


def ajax_copy_to_clipboard(request):
    api_key = None
    if request.user.is_staff:
        api_key = request.user.profile.api_key

    content = request.POST.get('content')

    # build absolute uri for "copy to clipboard" API endpoint and
    # send content to it
    copy_to_clipboard_endpoint = request.build_absolute_uri(reverse('copy-to-clipboard'))
    response = requests.post(
        copy_to_clipboard_endpoint,
        headers={'authorization': api_key},  # send user api_key ( if authenticated )
        data={'content': str(content)}
    )

    return JsonResponse(response.json(), status=200)


def logout(request):
    logout_user(request)
    return redirect('control')
