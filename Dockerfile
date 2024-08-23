FROM python:3.10

ENV POETRY_VERSION=1.8.3

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY clever clever
COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

RUN poetry config virtualenvs.create false

RUN poetry install

CMD uvicorn clever.router:app --host 0.0.0.0 --port 80
