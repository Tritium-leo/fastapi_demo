FROM python:3.8.13-slim-bullseye

RUN python -m pip install --upgrade pip

RUN mkdir /app

COPY . /app

RUN cd /app && pip install -r ./requirements.txt

WORKDIR /app

