FROM python:3.11-slim as base

WORKDIR /code

RUN apt update
RUN apt install -y gcc libpq-dev

FROM base

COPY . .
RUN pip install -r requirements.txt
