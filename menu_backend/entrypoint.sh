#!/bin/sh
set -e

/app/BruinBite/menu/manage.py collectstatic
/app/BruinBite/menu/manage.py makemigrations scraper
/app/BruinBite/menu/manage.py migrate
/app/BruinBite/menu/manage.py test --no-input

if [ $DJANGO_ENV == "prod" ]; then
    uwsgi --ini /app/BruinBite/menu/uwsgi.ini
else
    /app/BruinBite/menu/manage.py runserver 0.0.0.0:8000
fi

exec "$@"
