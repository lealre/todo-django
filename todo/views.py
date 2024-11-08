from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Case, IntegerField, When
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.urls import reverse

from todo.forms import TodoForm
from todo.models import Todo


def home(request):
    return render(request, 'todo/pages/home.html')


@login_required(login_url='users:login', redirect_field_name='next')
def todo_view(request):
    todos = (
        Todo.objects.filter(
            author__username=request.user.username, state__in=['done', 'todo']
        )
        .annotate(
            order_field=Case(
                When(state='done', then=1),
                When(state='todo', then=0),
                output_field=IntegerField(),
            )
        )
        .order_by('order_field', '-created_at', 'id')
    )

    paginator = Paginator(todos, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = TodoForm()
    todo_form_data = request.session.get('todo_form_data', None)
    form = TodoForm(todo_form_data)

    return render(
        request,
        'todo/pages/todo_view.html',
        context={'todos': page_obj, 'form': form},
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

        del request.session['todo_form_data']

        return redirect('todo:todo_list')

    return HttpResponseBadRequest('Error creating the todo item.')


@login_required(login_url='users:login', redirect_field_name='next')
def update_todo_state(request):
    if request.method == 'POST':
        todo_id = request.POST.get('id')
        new_state = request.POST.get('state')
        page_number = request.POST.get('page', 1)

        try:
            todo = Todo.objects.get(id=todo_id)
            todo.state = new_state
            todo.save()

            base_url = reverse('todo:todo_list')
            return redirect(f'{base_url}?page={page_number}')
        except Todo.DoesNotExist:
            return HttpResponseBadRequest('Todo not found.')

    return HttpResponseBadRequest('Invalid request method.')


@login_required(login_url='users:login', redirect_field_name='next')
def trash_todo(request):
    if request.method == 'POST':
        todo_id = request.POST.get('id')
        page_number = request.POST.get('page', 1)

        try:
            todo = Todo.objects.get(id=todo_id)

            if todo.state == 'trash':
                todo.state = 'todo'
                todo.save()
                base_url = reverse('todo:trash_view')
                return redirect(f'{base_url}?page={page_number}')

            todo.state = 'trash'
            todo.save()
            base_url = reverse('todo:todo_list')
            return redirect(f'{base_url}?page={page_number}')

        except Todo.DoesNotExist:
            return HttpResponseBadRequest('Todo not found.')

    return HttpResponseBadRequest('Invalid request method.')


@login_required(login_url='users:login', redirect_field_name='next')
def trash_view(request):
    todos = Todo.objects.filter(
        author__username=request.user.username, state='trash'
    )

    paginator = Paginator(todos, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request, 'todo/pages/trash.html', context={'todos': page_obj}
    )


@login_required(login_url='users:login', redirect_field_name='next')
def delete_todo(request):
    if request.method == 'POST':
        todo_id = request.POST.get('id')
        page_number = request.POST.get('page', 1)

        try:
            todo = Todo.objects.get(id=todo_id)
            todo.delete()
            base_url = reverse('todo:trash_view')
            return redirect(f'{base_url}?page={page_number}')
        except Todo.DoesNotExist:
            return HttpResponseBadRequest('Todo not found.')

    return HttpResponseBadRequest('Invalid request method.')


@login_required(login_url='users:login', redirect_field_name='next')
def update_todo_title(request):
    if request.method == 'POST':
        todo_id = request.POST.get('id')
        page_number = request.POST.get('page', 1)
        new_title = request.POST.get('title')

        try:
            todo = Todo.objects.get(id=todo_id)
            todo.title = new_title
            todo.save()
            base_url = reverse('todo:todo_list')
            return redirect(f'{base_url}?page={page_number}')
        except Todo.DoesNotExist:
            return HttpResponseBadRequest('Todo not found.')

    return HttpResponseBadRequest('Invalid request method.')
