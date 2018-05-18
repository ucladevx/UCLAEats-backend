#!/bin/bash

/app/BruinBite/menu/manage.py crontab add
/app/BruinBite/menu/manage.py makemigrations scraper
/app/BruinBite/menu/manage.py migrate
/app/BruinBite/menu/manage.py test

uwsgi --ini /app/BruinBite/menu/uwsgi.ini
