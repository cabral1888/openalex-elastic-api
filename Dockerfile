# syntax=docker/dockerfile:1.4
FROM python:3.10

WORKDIR /code

COPY . /code/
RUN apt install libpq-dev
RUN pip3 install -r requirements.txt