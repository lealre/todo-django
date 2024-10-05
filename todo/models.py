from django.contrib.auth.models import User
from django.db import models
from django.forms import ValidationError


class Todo(models.Model):
    class TodoChoices(models.TextChoices):
        TO_DO = 'todo'
        IN_PROGRESS =  'in_progress'
        DONE = 'done'
        TRASHED = 'trashed'

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=12, choices=TodoChoices, default=TodoChoices.TO_DO)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    def __str__(self) -> str:
        return self.title
    
    def clean(self):  
        choice_options = self.TodoChoices.values

        if self.state not in choice_options:
            raise ValidationError(
                f'"{self.state}" is not a valid choice for state.'
                f'Valid options are: {choice_options}.'
            )
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

