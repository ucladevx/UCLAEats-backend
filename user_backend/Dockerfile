FROM python:3.6

RUN apt-get update && \
    apt-get install -y && \
    pip3 install uwsgi

RUN mkdir -p /app/BruinBite/users

COPY . /app/BruinBite/users

RUN cd /app/BruinBite/users && pip3 install -r \
    /app/BruinBite/users/requirements.txt

EXPOSE 8000

RUN chmod +x /app/BruinBite/users/entrypoint.sh

ENTRYPOINT ["/app/BruinBite/users/entrypoint.sh"]
