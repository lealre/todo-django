from django.shortcuts import render

from .models import Todo


def home(requests):

    todos = Todo.objects.all()

    return render(
        requests,
        'global/base.html',
        context = {'todos': todos}
    )
    # return HttpResponse('My ToDo List')