from django.urls import reverse

from todo.tests.test_todo_base import TodoBase


class TodoUpdateStateTest(TodoBase):
    def test_update_todo_state_correctly(self):
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

    def test_update_todo_with_wrong_method(self):
        self.make_todo()
        title_expected = 'Invalid request method.'

        response = self.client.get(reverse('todo:update_state'))
        content = response.content.decode('utf-8')

        self.assertEqual(response.status_code, 400)
        self.assertIn(title_expected, content)

    def test_update_todo_with_id_non_existing(self):
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

    def test_delete_todo_successfully(self):
        todo = self.make_todo()

        response = self.client.post(
            reverse('todo:delete_todo'),
            data = {'id': todo.id}
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('todo:todo_list'))

        todo.refresh_from_db()
        is_deleted = self.exist_in_database(todo.id)
        self.assertTrue(is_deleted)

    # ToDo: test case where user is not loggedIn