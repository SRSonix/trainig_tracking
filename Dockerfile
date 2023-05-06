# syntax=docker/dockerfile:1

FROM python:3.11
WORKDIR /code
COPY ./app/pyproject.toml /code/pyproject.toml
COPY ./app/poetry.lock /code/poetry.lock
#RUN pip install --upgrade pip && pip install poetry
#RUN poetry install
