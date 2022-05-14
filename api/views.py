from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError

from config.models import Command

from utils.api.tools import save_received_request, api_response, get_request_data, get_search_query
from utils.core import http_status as sc
from utils.core.tools import execute_command
from utils.auth.http.decorators import login_required


@require_POST
@csrf_exempt
@login_required(api_endpoint=True)
def exec_command(request):

    data = get_request_data(request)

    command = data.get('command')

    if not command:
        return api_response(
            request,
            status_code=sc.HTTP_400_BAD_REQUEST,
            message='no command provided',
        )

    try:
        command = Command.objects.get(short_code=command)
    except Command.DoesNotExist:
        return api_response(
            request,
            status_code=sc.HTTP_404_NOT_FOUND,
            message='command is not valid'
        )

    if not command.active:
        return api_response(
            request,
            status_code=sc.HTTP_404_NOT_FOUND,
            message='command is not active'
        )

    # == ATTENTION ==
    # if command results in shutting down/sleep/hibernate etc. output won't save
    # == ATTENTION ==

    response = api_response(
        request,
        data={'command': command.command},
        status=True,
        commit=False,
        return_json=True
    )

    status_code = response['meta']['code']

    request_object = save_received_request(request, response, status_code=status_code)

    output = execute_command(command.command)
    response['data'] |= {'output': str(output) or None}

    request_object.response = response
    request_object.save()

    return JsonResponse(response, status=status_code)


@require_POST
@csrf_exempt
@login_required(api_endpoint=True)
def list_commands(request):

    search_fields = ['active', 'buttons__active']
    search_query = get_search_query(search_fields, get_request_data(request))

    commands = Command.objects.order_by('active', 'buttons__active').all()

    try:
        commands = commands.filter(**search_query)
    except ValidationError:
        pass  # ignore searches

    data = {}

    for cmd in commands:
        data[cmd.pk] = {
            'title': cmd.title,
            'command': cmd.command,
            'short_code': cmd.short_code,
            'description': cmd.description,
            'active': cmd.active,
            'has_buttons': False,
            'buttons': {},
        }

        if cmd.buttons.exists():
            data[cmd.pk]['has_buttons'] = True

            for btn in cmd.buttons.all():
                data[cmd.pk]['buttons'][btn.pk] = {
                    'color': btn.color,
                    'active': btn.active,
                }

    return api_response(request, data, commit=True)
