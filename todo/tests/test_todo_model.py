from django.core.exceptions import ValidationError
from parameterized import parameterized

from todo.tests.test_todo_base import TodoBase


class TodoModelTest(TodoBase):
    def setUp(self) -> None:
        self.todo = self.make_todo()
        self.todo_choices = self.todo.TodoChoices.values
        return super().setUp()

    def test_todo_title_string_representaion(self):
        self.todo.title = 'Test title'

        self.assertEqual(str(self.todo), self.todo.title)

    def test_todo_title_length_is_max_50_chars(self):
        self.todo.title = 'T' * 51

        with self.assertRaises(ValidationError):
            self.todo.full_clean()

    def test_todo_description_length_is_max_200_chars(self):
        self.todo.description = 'T' * 201

        with self.assertRaises(ValidationError):
            self.todo.full_clean()

    @parameterized.expand([
        ('todo'),
        ('in_progress'),
        ('done'),
        ('trash'),
    ])
    def test_todo_state_must_be_in_todo_choices_options(self, value):
        self.todo.state = value

        self.assertIn(value, self.todo_choices)
        self.todo.save()

    def test_todo_state_not_in_todo_choices_raises_validation_error(self):
        state = 'wrong'

        self.todo.state = state

        with self.assertRaises(ValidationError):
            self.todo.clean()
