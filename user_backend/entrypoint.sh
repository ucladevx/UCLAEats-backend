#!/bin/sh
set -e

/app/BruinBite/users/manage.py makemigrations users
/app/BruinBite/users/manage.py makemigrations chat
/app/BruinBite/users/manage.py makemigrations matching
/app/BruinBite/users/manage.py migrate
#/app/BruinBite/users/manage.py test --no-input

if [ $DJANGO_ENV == "prod" ]; then
#    uwsgi --ini /app/BruinBite/users/uwsgi.ini
    daphne user_backend.asgi:channel_layer --port 8888
else
    /app/BruinBite/users/manage.py runserver 0.0.0.0:8000
#    /app/BruinBite/messaging/manage.py runserver 0.0.0.0:8888
fi

exec "$@"
