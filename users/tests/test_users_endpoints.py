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
        self.assertTrue(response.wsgi_request.user.is_authenticated)

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

    def test_endpoint_logout_successfully(self):
        user = self.create_user_in_db()
        message_expected = 'Logged out successfully'
        url_to_redirect = reverse('todo:home')

        response = self.client.post(
            reverse('users:logout'),
            data={'username': user.username},
            follow=True,
        )
        messages = list(response.context['messages'])

        self.assertRedirects(response, url_to_redirect)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertTrue(
            any(message_expected in str(message) for message in messages)
        )

    def test_endpoint_logout_redirects_if_not_logged_in(self):
        user = self.create_user_in_db(is_authenticated=False)
        url_to_redirect = reverse('users:login')
        original_endpoint = reverse('users:logout')
        complete_url_after_redirect = (
            f'{url_to_redirect}?next={original_endpoint}'
        )

        response = self.client.post(
            original_endpoint, data={'username': user.username}, follow=True
        )

        self.assertRedirects(response, complete_url_after_redirect)

    def test_endpoint_logout_with_wrong_method(self):
        self.create_user_in_db()
        message_expected = 'Wrong method to url'
        # Redirects to login, which then redirects to home
        url_to_redirect = reverse('todo:home')
        original_endpoint = reverse('users:logout')

        response = self.client.get(original_endpoint, follow=True)
        messages = list(response.context['messages'])

        self.assertRedirects(response, url_to_redirect)
        self.assertTrue(
            any(message_expected in str(message) for message in messages)
        )

    def test_endpoint_logout_with_wrong_user_credentials(self):
        self.create_user_in_db()
        message_expected = 'Invalid logout user'
        # Redirects to login, which then redirects to home
        url_to_redirect = reverse('todo:home')
        original_endpoint = reverse('users:logout')

        response = self.client.post(
            original_endpoint, data={'username': 'wrong_user'}, follow=True
        )

        messages = list(response.context['messages'])

        self.assertRedirects(response, url_to_redirect)
        self.assertTrue(
            any(message_expected in str(message) for message in messages)
        )

    def test_endpoint_register_create_with_wrong_method(self):
        self.create_user_in_db()
        message_expected = 'Invalid request method.'

        response = self.client.get(
            reverse('users:register_validate'), follow=True
        )
        content = response.content.decode('utf-8')

        self.assertTrue(response.status_code, 400)
        self.assertIn(message_expected, content)
