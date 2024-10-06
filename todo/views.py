from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render

from .models import Todo


def home(requests):
    todos = Todo.objects.all()

    return render(requests, 'global/base.html', context={'todos': todos})


def update_todo_state(request):
    if request.method == 'POST':
        todo_id = request.POST.get('id')
        new_state = request.POST.get('state')

        try:
            todo = Todo.objects.get(id=todo_id)
            todo.state = new_state
            todo.save()
            return redirect('todo:home')
        except Todo.DoesNotExist:
            return HttpResponseBadRequest('Todo not found.')

    return HttpResponseBadRequest('Invalid request method.')
