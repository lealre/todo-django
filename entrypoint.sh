#!/bin/bash

python manage.py migrate --noinput 

# Check if the superuser already exists
if python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.filter(username='${SUPERUSER_USERNAME}').exists())" | grep -q "True"; then
    echo "Superuser already exists."
else
    # Create superuser
    python manage.py createsuperuser --noinput --username "${SUPERUSER_USERNAME}" --email "${SUPERUSER_EMAIL}"
    # Set password for the superuser
    python manage.py shell -c "from django.contrib.auth.models import User; user = User.objects.get(username='${SUPERUSER_USERNAME}'); user.set_password('${SUPERUSER_PASSWORD}'); user.save()"
    echo "Superuser created with username '${SUPERUSER_USERNAME}'."
fi

python manage.py collectstatic --noinput

python manage.py runserver 0.0.0.0:8000