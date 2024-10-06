from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render

from todo.models import Todo, User
from todo.forms import TodoForm


def home(request):
    todos = Todo.objects.all()

    form = TodoForm()
    todo_form_data = request.session.get('todo_form_data', None)
    form = TodoForm(todo_form_data)

    return render(
        request, 
        'todo/pages/home.html', 
        context={
            'todos': todos,
            'form': form
        })


def create_todo(request):
    if not request.POST:
          return HttpResponseBadRequest('Invalid request method.')
    
    POST = request.POST
    request.session['todo_form_data'] = POST
    form = TodoForm(POST)

    if form.is_valid():
            # Don't commit yet; we will assign a mock author
        todo = form.save(commit=False)

        # Fetch a "mock" author from the database (example: first user)
        mock_author = User.objects.first()  # You can choose any logic here
        
        # Assign the "mock" author
        todo.author = mock_author

        form.save()
        messages.success(request, 'ToDo added to List')
        del request.session['todo_form_data']
    
    return redirect('todo:home')


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
