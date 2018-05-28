#!/bin/sh

cd /app/BruinBite/messaging && ./manage.py makemigrations 
cd /app/BruinBite/messaging && ./manage.py migrate

if [ $DJANGO_ENV == "prod" ]; then
    daphne chat.asgi:channel_layer --port 8888
    /app/BruinBite/messaging/manage.py runworker
else
    echo "Development Environment"
    /app/BruinBite/messaging/manage.py runserver 0.0.0.0:8888
fi
