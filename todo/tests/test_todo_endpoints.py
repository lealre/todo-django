from django.urls import reverse

from todo.tests.test_todo_base import TodoBase


class TodoEndpointsTest(TodoBase):
    def test_endpoint_create_todo_successfully(self):
        self.make_author()  # Authenticate first
        title_expected = 'test title'

        response = self.client.post(
            reverse('todo:create'), data={'title': title_expected}
        )

        todo_created = self.get_todo_by_id(id=1)

        self.assertEqual(todo_created.title, title_expected)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('todo:todo_list'))

    def test_endpoint_create_todo_with_wrong_method(self):
        self.make_author()  # Authenticate first
        message_expected = 'Invalid request method.'

        response = self.client.get(reverse('todo:create'))
        content = response.content.decode('utf-8')

        self.assertEqual(response.status_code, 400)
        self.assertIn(message_expected, content)

    def test_endpoint_create_todo_with_form_not_valid(self):
        self.make_author()  # Authenticate first
        title_expected = 'T' * 51  # title max_length = 50
        message_expected = 'Error creating the todo item.'

        response = self.client.post(
            reverse('todo:create'), data={'title': title_expected}
        )
        content = response.content.decode('utf-8')

        self.assertEqual(response.status_code, 400)
        self.assertIn(message_expected, content)

    def test_endpoint_create_todo_not_authenticated(self):
        self.make_todo(is_authenticated=False)
        title_expected = 'test title'
        original_endpoint = reverse('todo:create')
        endpoint_to_redirect = reverse('users:login')

        response = self.client.post(
            reverse('todo:create'),
            data={'title': title_expected},
        )

        self.assertEqual(response.status_code, 302)
        redicrect_login_url = (
            f'{endpoint_to_redirect}?next={original_endpoint}'
        )
        self.assertRedirects(response, redicrect_login_url)

    def test_endpoint_update_todo_state_successfully(self):
        todo = self.make_todo()
        new_state = 'done'

        response = self.client.post(
            reverse('todo:update_state'),
            data={'id': todo.id, 'state': new_state},
        )
        todo.refresh_from_db()

        self.assertEqual(todo.state, 'done')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('todo:todo_list'))

    def test_endpoint_update_todo_state_with_wrong_method(self):
        self.make_todo()
        title_expected = 'Invalid request method.'

        response = self.client.get(reverse('todo:update_state'))
        content = response.content.decode('utf-8')

        self.assertEqual(response.status_code, 400)
        self.assertIn(title_expected, content)

    def test_endpoint_update_todo_state_with_id_non_existing(self):
        todo = self.make_todo()
        new_state = 'done'
        title_expected = 'Todo not found.'

        response = self.client.post(
            reverse('todo:update_state'),
            data={'id': todo.id + 100, 'state': new_state},
        )
        todo.refresh_from_db()

        content = response.content.decode('utf-8')

        self.assertEqual(response.status_code, 400)
        self.assertIn(title_expected, content)

    def test_endpoint_update_todo_state_not_authenticated(self):
        todo = self.make_todo(is_authenticated=False)
        new_state = 'done'
        original_endpoint = reverse('todo:update_state')
        endpoint_to_redirect = reverse('users:login')

        response = self.client.post(
            reverse('todo:update_state'),
            data={'id': todo.id, 'state': new_state},
        )
        todo.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        redicrect_login_url = (
            f'{endpoint_to_redirect}?next={original_endpoint}'
        )
        self.assertRedirects(response, redicrect_login_url)

    def test_endpoint_trash_todo_successfully(self):
        todo = self.make_todo()
        expected_state = 'trash'

        response = self.client.post(
            reverse('todo:trash_todo'),
            data={'id': todo.id},
        )
        todo.refresh_from_db()

        self.assertEqual(todo.state, expected_state)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('todo:todo_list'))

    def test_endpoint_trash_todo_with_wrong_method(self):
        self.make_todo()
        title_expected = 'Invalid request method.'

        response = self.client.get(
            reverse('todo:trash_todo'),
        )

        content = response.content.decode('utf-8')

        self.assertEqual(response.status_code, 400)
        self.assertIn(title_expected, content)

    def test_endpoint_trash_todo_with_id_non_existing(self):
        todo = self.make_todo()
        title_expected = 'Todo not found.'

        response = self.client.post(
            reverse('todo:trash_todo'),
            data={'id': todo.id + 100},
        )
        todo.refresh_from_db()

        content = response.content.decode('utf-8')

        self.assertEqual(response.status_code, 400)
        self.assertIn(title_expected, content)

    def test_endpoint_trash_todo_state_not_authenticated(self):
        todo = self.make_todo(is_authenticated=False)
        original_endpoint = reverse('todo:trash_todo')
        endpoint_to_redirect = reverse('users:login')

        response = self.client.post(
            reverse('todo:trash_todo'),
            data={'id': todo.id},
        )
        todo.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        redicrect_login_url = (
            f'{endpoint_to_redirect}?next={original_endpoint}'
        )
        self.assertRedirects(response, redicrect_login_url)

    def test_endpoint_trash_todo_restoring_from_trash_successfully(self):
        todo = self.make_todo(state='trash')
        expected_state = 'todo'

        response = self.client.post(
            reverse('todo:trash_todo'),
            data={'id': todo.id},
        )
        todo.refresh_from_db()

        self.assertEqual(todo.state, expected_state)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('todo:trash_view'))

    def test_endpoint_delete_todo_from_trash_successfully(self):
        todo = self.make_todo(state='trash')

        response = self.client.post(
            reverse('todo:delete_todo'),
            data={'id': todo.id},
        )
        is_todo_in_database = self.exist_in_database(id=todo.id)

        self.assertFalse(is_todo_in_database)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('todo:trash_view'))

    def test_endpoint_delete_todo_from_trash_with_wrong_method(self):
        self.make_todo(state='trash')
        title_expected = 'Invalid request method.'

        response = self.client.get(
            reverse('todo:delete_todo'),
        )

        content = response.content.decode('utf-8')

        self.assertEqual(response.status_code, 400)
        self.assertIn(title_expected, content)

    def test_endpoint_delete_todo_from_trash_with_id_non_existing(self):
        todo = self.make_todo(state='trash')
        title_expected = 'Todo not found.'

        response = self.client.post(
            reverse('todo:delete_todo'),
            data={'id': todo.id + 100},
        )
        todo.refresh_from_db()

        content = response.content.decode('utf-8')

        self.assertEqual(response.status_code, 400)
        self.assertIn(title_expected, content)

    def test_endpoint_delete_todo_from_trash_not_authenticated(self):
        todo = self.make_todo(is_authenticated=False)
        original_endpoint = reverse('todo:delete_todo')
        endpoint_to_redirect = reverse('users:login')

        response = self.client.post(
            reverse('todo:delete_todo'),
            data={'id': todo.id},
        )
        todo.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        redicrect_login_url = (
            f'{endpoint_to_redirect}?next={original_endpoint}'
        )
        self.assertRedirects(response, redicrect_login_url)
