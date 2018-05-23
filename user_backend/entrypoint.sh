#!/bin/sh

cd /app/BruinBite/users && ./manage.py makemigrations users
cd /app/BruinBite/users && ./manage.py makemigrations matching
cd /app/BruinBite/users && ./manage.py migrate
cd /app/BruinBite/users && ./manage.py test --no-input
uwsgi --ini /app/BruinBite/users/uwsgi.ini
