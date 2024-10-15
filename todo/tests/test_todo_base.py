from django.test import TestCase

from todo.models import Todo, User


class TodoBase(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def make_author(  # noqa: PLR0913, PLR0917
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

    def make_todo(  # noqa: PLR0917
        self,
        title='task title',
        description='task description',
        state='todo',
        author_data: dict = {},
        is_authenticated: bool = True,
    ):
        return Todo.objects.create(
            title=title,
            description=description,
            state=state,
            author=self.make_author(
                **author_data, is_authenticated=is_authenticated
            ),
        )

    def exist_in_database(self, id: int) -> bool:  # noqa: PLR6301
        return Todo.objects.filter(id=id).exists()

    def get_todo_by_id(self, id: int):  # noqa: PLR6301
        return Todo.objects.get(id=id)
