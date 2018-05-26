#!/bin/sh
set -e

/app/BruinBite/menu/manage.py crontab add

crond -f

exec "$@"
