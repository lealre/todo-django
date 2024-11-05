# "Hello Wolrd" with Django - A to-do app

This repository contains a basic to-do app built with the Django framework. It features a simple interface to add, edit, and delete to-dos. In the trash area, you can either restore a to-do or permanently delete it.

To perform operations, the user must be authenticated by registering and logging into the application.

<-- video here -->

Among the many features of Django, this project uses:

- [Django Forms](https://docs.djangoproject.com/en/5.1/ref/forms/)
- [Django Messages](https://docs.djangoproject.com/en/5.1/ref/contrib/messages/)
- [Django Authentication System](https://docs.djangoproject.com/en/5.1/topics/auth/default/)
- [Django Pagination](https://docs.djangoproject.com/en/5.1/topics/pagination/)
- [Django Testing](https://docs.djangoproject.com/en/5.1/topics/testing/overview/)

It uses function-based views and includes some JavaScript to enable frontend interactions.

Although it does not test every aspect of the application, it achieves 100% coverage using [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/). The tests also utilize [pytest](https://docs.pytest.org/en/stable/).

It’s possible to run this app using Docker Compose, which automatically creates a superuser and uses a local PostgreSQL database. The PostgreSQL database is also set up within Docker Compose.

## How it works

User Registration

...

Login and usage

...

Trash

...

## How to run this project

All the steps here were intended to a `bash` terminal.

This section shows how to run the project both with Docker or locally. Regardless of the method, start with the following steps:

1 - Clone the repo locally:

```bash
git clone https://github.com/lealre/todo-django.git
```

2 - Access the project directory:

```bash
cd todo-django
```

### Docker Environment

[How to install Docker Compose](https://docs.docker.com/compose/install/)

3 - Create the `.env` file:

```bash
mv .env-example .env
```

By using the variables from [`.env-example`](.env-example), it will connect to the PostgreSQL database that was also created with Docker.

4 - Build and start the container:

```bash
docker compose up --build -d
```

In case you encounter a permission error for `entrypoint.sh`, run:

```bash
chmod +x entrypoint.sh
```

Access the application at http://localhost:8000/

### Local Environment

The project setup uses [`pyenv`](https://github.com/pyenv/pyenv) and [`poetry`](https://python-poetry.org/).

After completing steps 1 and 2:

3 - Create the `.env` file:

```bash
mv .env-example .env
```

In the local environment, SQLite3 is used by default, so it's necessary to set `LOCAL` in the `.env` file:

```
LOCAL=1
```

4 - Set the Python version with `pyenv`:

```bash
pyenv local 3.12.2
```

5 - Create the virtual environment:

```bash
poetry env use 3.12.2
```

6 - Activate the virtual environment:

```bash
poetry shell
```

7 - Install dependencies:

```bash
poetry install --no-root
```

8 - Run the migrations:

```bash
python manage.py migrate
```

9 - Run the server:

```bash
python manage.py runserver
```

Access the application at http://localhost:8000/