from django.urls import reverse

from users.tests.test_users_base import UsersBase


class UsersEndpointsTest(UsersBase):
    def test_endpoint_validate_login_successfully(self):
        password = 'Str0ngP@ssword1'
        user = self.create_user_in_db(
            is_authenticated=False, password=password
        )
        url_to_redirect = reverse('todo:todo_list')

        response = self.client.post(
            reverse('users:validate_user'),
            data={'username': user.username, 'password': password},
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, url_to_redirect)

    def test_endpoint_validate_login_invalid_credentials(self):
        message_expected = 'Invalid credentials'
        password = 'Str0ngP@ssword1'
        url_to_redirect = reverse('users:login')
        user = self.create_user_in_db(
            is_authenticated=False, password=password
        )

        response = self.client.post(
            reverse('users:validate_user'),
            data={'username': user.username, 'password': 'wrong_password'},
            follow=True,
        )
        messages = list(response.context['messages'])

        self.assertRedirects(response, url_to_redirect)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertTrue(
            any(message_expected in str(message) for message in messages)
        )

    def test_endpoint_validate_login_invalid_forms_inputs(self):
        message_expected = 'Invalid username or password'
        url_to_redirect = reverse('users:login')

        response = self.client.post(
            reverse('users:validate_user'),
            data={'username': '', 'password': ''},
            follow=True,
        )
        messages = list(response.context['messages'])

        self.assertRedirects(response, url_to_redirect)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertTrue(
            any(message_expected in str(message) for message in messages)
        )

    def test_endpoint_validate_login_with_wrong_method(self):
        message_expected = 'Wrong method to url'

        response = self.client.get(reverse('users:validate_user'))
        content = response.content.decode('utf-8')

        self.assertEqual(response.status_code, 400)
        self.assertIn(content, message_expected)
