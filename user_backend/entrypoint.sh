#!/bin/bash

cd /app/BruinBite/users && ./manage.py makemigrations users
cd /app/BruinBite/users && ./manage.py migrate
cd /app/BruinBite/users && ./manage.py test
uwsgi --ini /app/BruinBite/users/uwsgi.ini
