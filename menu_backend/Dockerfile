FROM python:3.6

RUN apt-get update && \
    apt-get install -y && \
    pip3 install uwsgi

RUN apt-get install -y cron

RUN mkdir -p /app/BruinBite/menu

COPY . /app/BruinBite/menu

RUN cd /app/BruinBite/menu && pip3 install -r \
    /app/BruinBite/menu/requirements.txt

EXPOSE 8000

RUN chmod +x /app/BruinBite/menu/entrypoint.sh

ENTRYPOINT ["/app/BruinBite/menu/entrypoint.sh"]
