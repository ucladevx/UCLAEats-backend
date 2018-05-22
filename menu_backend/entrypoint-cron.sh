#!/bin/sh
set -e

/app/BruinBite/menu/manage.py crontab add
/app/BruinBite/menu/manage.py makemigrations scraper
/app/BruinBite/menu/manage.py migrate

crond -f

exec "$@"
