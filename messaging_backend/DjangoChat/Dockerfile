FROM python:3.6-alpine

RUN apk add -U postgresql-dev gcc python3-dev musl-dev linux-headers \
    libffi-dev 

RUN mkdir -p /app/BruinBite/messaging

ADD ./requirements.txt /app/BruinBite/messaging

RUN pip3 install -r /app/BruinBite/messaging/requirements.txt

COPY . /app/BruinBite/messaging

RUN chmod +x /app/BruinBite/messaging/entrypoint.sh

WORKDIR /app/BruinBite/messaging
# ENTRYPOINT ["/app/BruinBite/messaging/entrypoint.sh"]
