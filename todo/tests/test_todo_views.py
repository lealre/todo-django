"""
This module tests what is rendered on the user's screen.
"""

from django.urls import resolve, reverse

from todo import views
from todo.tests.test_todo_base import TodoBase


class TodoViewTest(TodoBase):
    def test_todo_home_view_funcion_is_correct(self):
        view = resolve(reverse('todo:home'))

        self.assertIs(view.func, views.home)

    def test_todo_home_view_loads_correct_template_and_status_200_OK(self):
        response = self.client.get(reverse('todo:home'))

        self.assertTemplateUsed(response, 'todo/pages/home.html')
        self.assertEqual(response.status_code, 200)

    def test_todo_home_template_message_when_not_logged_in(self):
        self.make_todo(is_authenticated=False)

        response = self.client.get(reverse('todo:home'))
        content = response.content.decode('utf-8')

        self.assertIn('You are not logged in.', content)

    def test_todo_home_template_message_when_logged_in(self):
        todo = self.make_todo()

        username = todo.author.username

        response = self.client.get(reverse('todo:home'))
        content = response.content.decode('utf-8')

        self.assertIn(f'You are already logged in  as {username}.', content)
