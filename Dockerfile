# syntax=docker/dockerfile:1

FROM python:3.11
WORKDIR /code
COPY ./pyproject.toml /code/pyproject.toml
COPY ./poetry.lock /code/poetry.lock
#RUN pip install --upgrade pip && pip install poetry
#RUN poetry install
#COPY ./app /code/app

#CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8080"]
