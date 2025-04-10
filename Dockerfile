# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12.3

FROM python:${PYTHON_VERSION}-slim AS base

ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_DB

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Poetry env
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VERSION=1.8.2

WORKDIR /app

# Install Poetry - a dependency management and packaging tool for Python
RUN pip install poetry==${POETRY_VERSION}


# Copy the pyproject.toml and poetry.lock files to leverage Docker caching
COPY pyproject.toml poetry.lock ./

# Install dependencies with Poetry
RUN poetry install --only main

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

CMD echo "Environment: ${ENV}"; \
    echo "Apply database migrations" && alembic upgrade head; \
    echo "Starting server" && poetry run uvicorn 'server.app:app' --host=0.0.0.0 --port=8000
