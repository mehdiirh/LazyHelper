from django.shortcuts import render, reverse, redirect
from django.contrib.auth import logout as logout_user

from config.models import Button

from utils.auth.http.decorators import login_required

import json
import requests


@login_required(redirect_login=True, next_redirect='control')
def control(request):

    custom_buttons = Button.objects.filter(active=True, command__active=True).all()
    context = {
        'response': '',
        'custom_buttons': custom_buttons,
        'user': request.user,
    }

    api_key = None
    if request.user.is_staff:
        api_key = request.user.profile.api_key

    if request.method == 'POST':
        command = request.POST.get('command')

        # build absolute uri for "command execution" API endpoint and
        # send command to it
        execute_command_endpoint = request.build_absolute_uri(reverse('exec-command'))
        response = requests.post(
            execute_command_endpoint,
            headers={'authorization': api_key},  # send user api_key ( if authenticated )
            data={'command': str(command)}
        )

        try:
            response = response.json()
            _data = response['data'] or {}
            output = _data.get('output')
        except json.JSONDecodeError:
            output = f'ERROR:\n{str(response.status_code)} {str(response.reason)}'

        context['response'] = output

    return render(request, 'control/main.html', context=context)


def logout(request):
    logout_user(request)
    return redirect('control')
