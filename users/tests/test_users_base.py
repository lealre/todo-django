from django.test import TestCase

from todo.models import User


class UsersBase(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def create_user_in_db(  # noqa: PLR0913, PLR0917
        self,
        first_name='user',
        last_name='name',
        username='username',
        password='123456',
        email='username@email.com',
        is_authenticated: bool = True,
    ):
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

        if is_authenticated:
            self.client.login(username=username, password=password)

        return user
