from django.test import TestCase

from todo.models import Todo, User


class TodoBase(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def make_author(  # noqa: PLR6301
        self,
        first_name='user',
        last_name='name',
        username='username',
        password='123456',
        email='username@email.com',
    ):
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

        self.client.login(username=username, password=password)

        return user

    def make_todo(
        self,
        title='task title',
        description='task description',
        state='todo',
        author_data: dict = {},
    ):
        return Todo.objects.create(
            title=title,
            description=description,
            state=state,
            author=self.make_author(**author_data),
        )
    
    def exist_in_database(self, todo_id: int) -> bool:
        return Todo.objects.filter(id=todo_id).exists()
