#!/bin/bash

/app/BruinBite/menu/manage.py makemigrations menu
/app/BruinBite/menu/manage.py migrate
/app/BruinBite/menu/manage.py test

uwsgi --ini /app/BruinBite/menu/uwsgi.ini
