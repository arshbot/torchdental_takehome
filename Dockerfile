FROM python:3.8-slim-buster

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install python3-dev gcc musl-dev -y && \
    apt-get clean

RUN pip install --upgrade pip
RUN pip install psycopg2-binary
COPY ./requirements.txt /tmp/requirements.txt
RUN cd /tmp/ && pip install -r requirements.txt

COPY torchdental_takehome /app/torchdental_takehome

