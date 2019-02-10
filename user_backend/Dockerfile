FROM python:3.6-alpine

RUN apk add -U postgresql-dev gcc python3-dev musl-dev linux-headers \
    libffi-dev
        # libxslt-dev libxml2-dev

RUN pip3 install --upgrade uwsgi

RUN mkdir -p /app/BruinBite/users

ADD ./requirements.txt /app/BruinBite/users

RUN pip3 install -r /app/BruinBite/users/requirements.txt

COPY . /app/BruinBite/users

EXPOSE 8000

RUN chmod +x /app/BruinBite/users/entrypoint.sh

ENTRYPOINT ["/app/BruinBite/users/entrypoint.sh"]
