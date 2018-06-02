#!/bin/sh

cd /app/BruinBite/messaging && ./manage.py makemigrations
cd /app/BruinBite/messaging && ./manage.py migrate

if [ $DJANGO_ENV == "prod" ]; then
    echo "LOG -- Daphne Startup"
    daphne chat.asgi:channel_layer --port 8888
    # echo "LOG -- Running Worker"
    # /app/BruinBite/messaging/manage.py runworker
else
    echo "Development Environment"
    /app/BruinBite/messaging/manage.py runserver 0.0.0.0:8888
fi
