from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render

from todo.forms import TodoForm
from todo.models import Todo


def home(request):
    return render(request, 'todo/pages/home.html')


@login_required(login_url='users:login', redirect_field_name='next')
def todo_view(request):
    todos = Todo.objects.filter(author__username=request.user.username)

    form = TodoForm()
    todo_form_data = request.session.get('todo_form_data', None)
    form = TodoForm(todo_form_data)

    return render(
        request,
        'todo/pages/todo_view.html',
        context={'todos': todos, 'form': form},
    )


@login_required(login_url='users:login', redirect_field_name='next')
def create_todo(request):
    if not request.POST:
        return HttpResponseBadRequest('Invalid request method.')

    current_user = request.user

    POST = request.POST
    request.session['todo_form_data'] = POST
    form = TodoForm(POST)

    if form.is_valid():
        todo = form.save(commit=False)
        todo.author = current_user
        form.save()

        messages.success(request, 'ToDo added to List')

        del request.session['todo_form_data']

    return redirect('todo:todo_list')


def update_todo_state(request):
    if request.method == 'POST':
        todo_id = request.POST.get('id')
        new_state = request.POST.get('state')

        try:
            todo = Todo.objects.get(id=todo_id)
            todo.state = new_state
            todo.save()
            return redirect('todo:todo_list')
        except Todo.DoesNotExist:
            return HttpResponseBadRequest('Todo not found.')

    return HttpResponseBadRequest('Invalid request method.')
