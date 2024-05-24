FROM python:3.9-slim-buster

WORKDIR /app

ADD ./requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install gunicorn
RUN pip install -r requirements.txt

ADD ./manage.py /app/manage.py
ADD ./config /app/config
ADD ./scripts /app/scripts

RUN chmod +x /app/scripts/entry-server.sh
RUN chmod +x /app/scripts/entry-worker.sh
