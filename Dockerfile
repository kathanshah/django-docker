FROM python:3.8-alpine

MAINTAINER Tully

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /application
WORKDIR /application
COPY ./application /application

RUN adduser -D user
USER user