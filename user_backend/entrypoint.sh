#!/bin/bash

/app/BruinBite/users/manage.py makemigrations users
/app/BruinBite/users/manage.py migrate
/app/BruinBite/users/manage.py test

uwsgi --ini /app/BruinBite/users/uwsgi.ini
