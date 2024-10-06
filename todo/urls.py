from django.urls import path

from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.home, name='home'),
    path('update_state', views.update_todo_state, name='update_state'),
]
