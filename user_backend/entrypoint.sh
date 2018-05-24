#!/bin/sh

cd /app/BruinBite/users && ./manage.py makemigrations users
cd /app/BruinBite/users && ./manage.py makemigrations matching
cd /app/BruinBite/users && ./manage.py migrate
cd /app/BruinBite/users && ./manage.py test --no-input

if [ -z $DHANGO_ENV ]; then 
    if [ $DJANGO_ENV == "prod" ]; then
        uwsgi --ini /app/BruinBite/users/uwsgi.ini
    else
        ./manage.py runserver 0.0.0.0:8000
    fi
fi
