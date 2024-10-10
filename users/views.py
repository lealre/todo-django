from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import reverse

from users.form import LoginForm


def login_view(requests):
    form = LoginForm()

    return render(
        requests,
        'users/pages/login.html',
        context= {
            'form': form,
            'form_action': reverse('users:validate_user')
        }
    )


def validate_user(request):
    if not request.POST:
        return HttpResponse('Wrong method to url')
    
    form = LoginForm(request.POST)

    login_url_redirect = reverse('users:login')

    if form.is_valid():
        authenticated_user = authenticate(
            username = form.cleaned_data.get('username', ''),
            password = form.cleaned_data.get('password', ''),
        )

        if authenticated_user:
            login(request, authenticated_user)
            home_todo_url = reverse('todo:todo_list')
            return redirect(home_todo_url)
        
        messages.error(request, 'Invalid credentials')
        return redirect(login_url_redirect)
    
    messages.error(request, 'Invalid username or password')
    return redirect(login_url_redirect)
