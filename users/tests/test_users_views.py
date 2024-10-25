from django.urls import reverse

from users.tests.test_users_base import UsersBase


class UsersViewsTest(UsersBase):
    def test_login_url_redirect_if_user_is_already_logged_in(self):
        self.create_user_in_db()
        url_to_redirect = reverse('todo:home')

        response = self.client.get(reverse('users:login'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, url_to_redirect)
