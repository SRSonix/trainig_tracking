# syntax=docker/dockerfile:1

FROM python:3.11-slim
COPY poetry.lock pyproject.toml /
