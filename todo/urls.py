from django.urls import path

from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.home, name='home'),
    path('todo_list/', views.todo_view, name='todo_list'),
    path('update_state/', views.update_todo_state, name='update_state'),
    path('create_todo/', views.create_todo, name='create'),
    path('trash_todo/', views.trash_todo, name='trash_todo'),
    path('trash/', views.trash_view, name='trash_view'),
    # path('delete_todo', views.create_todo, name='delete_todo'),
]
