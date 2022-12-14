#!/bin/bash

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

# Create automatically superuser for moliuWeb
if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
fi

gunicorn moliu.wsgi --bind 0.0.0.0:8000

# Run, if any, the command passed in by the user on the command line
# and replace the currently running process with the new one
exec "$@"