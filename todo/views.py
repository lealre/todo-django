from django.shortcuts import render

from django.http import HttpResponse


def home(requests):

    todos = [
        {
            'title': f'Todo {n}',
            'description': f'Some task to do  {n}',
            'state': 'Pending'
        }
        for n in range(10)
    ]


    return render(
        requests,
        'global/base.html',
        context = {'todos': todos}
    )
    # return HttpResponse('My ToDo List')