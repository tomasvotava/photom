ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /code

RUN python -m pip install -q poetry==1.5.1

COPY poetry.lock pyproject.toml /code/

RUN poetry install --no-interaction --no-root

COPY . /code/

ENTRYPOINT ["poetry", "run"]
