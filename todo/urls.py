from django.urls import path

from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.home, name='home'),
    path('todos/', views.todo_view, name='todo_list'),
    path('todos/update/', views.update_todo_state, name='update_state'),
    path('todos/create/', views.create_todo, name='create'),
    path('todos/trashed/', views.trash_view, name='trash_view'),
    path('todos/trash/update', views.trash_todo, name='trash_todo'),
    path('todos/trashed/delete', views.delete_todo, name='delete_todo'),
]
