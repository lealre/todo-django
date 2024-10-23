from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized


class UserResgisterFormTest(TestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@anyemail.com',
            'password': 'Str0ngP@ssword1',
            'password2': 'Str0ngP@ssword1',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        'no_uppercase123',
        'NO_LOWERCASE123',
        'No_NumberIncluded',
    ])
    def test_equal_passwords_pattern_validation_error(self, pass_case):
        self.form_data['password'] = pass_case
        self.form_data['password2'] = pass_case
        error_message = (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        )

        response = self.client.post(
            reverse('users:register_validate'),
            data=self.form_data,
            follow=True,
        )

        self.assertIn(
            error_message, response.context['form'].errors.get('password')
        )

        self.assertIn(error_message, response.content.decode('utf-8'))

    def test_different_passwords_validation_error(self):
        self.form_data['password'] = 'Str0ngP@ssword_case1'
        self.form_data['password2'] = 'Str0ngP@ssword_case2'
        error_message = 'Password and password2 must be equal'

        response = self.client.post(
            reverse('users:register_validate'),
            data=self.form_data,
            follow=True
        )

        self.assertIn(
            error_message, response.context['form'].errors.get('password')
        )
        self.assertIn(error_message, response.content.decode('utf-8'))

    def test_equal_emails_error(self):
        error_message = 'User e-mail is already in use'

        self.client.post(
            reverse('users:register_validate'),
            data=self.form_data,
        )
        response = self.client.post(
            reverse('users:register_validate'),
            data=self.form_data,
            follow=True
        )

        self.assertIn(
            error_message, response.context['form'].errors.get('email')
        )
        self.assertIn(error_message, response.content.decode('utf-8'))
