from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from users.form import LoginForm


def login_view(request):
    form = LoginForm()

    if request.user.is_authenticated:
        messages.warning(
            request, f'You are already logged in as {request.user.username}'
        )
        return redirect(reverse('todo:home'))

    return render(
        request,
        'users/pages/login.html',
        context={'form': form, 'form_action': reverse('users:validate_user')},
    )


def validate_user(request):
    if not request.POST:
        return HttpResponse('Wrong method to url')

    form = LoginForm(request.POST)

    login_url_redirect = reverse('users:login')

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user:
            login(request, authenticated_user)
            todo_list_url = reverse('todo:todo_list')
            return redirect(todo_list_url)

        messages.error(request, 'Invalid credentials')
        return redirect(login_url_redirect)

    messages.error(request, 'Invalid username or password')
    return redirect(login_url_redirect)


@login_required(login_url='users:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, 'Invalid logout request')
        return redirect(reverse('users:login'))

    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid logout user')
        return redirect(reverse('users:login'))

    messages.success(request, 'Logged out successfully')
    logout(request)

    home_url = reverse('todo:home')
    return redirect(home_url)
