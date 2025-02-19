# Stage 1: Compile Python files
FROM python:3.11 AS builder

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Poetry Version
ENV POETRY_VERSION=1.7.1

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"

RUN pip3 install --upgrade pip
RUN pip3 install "poetry==$POETRY_VERSION"
COPY poetry.lock pyproject.toml /usr/src/app/
RUN poetry export -f requirements.txt --without-hashes --output /usr/src/app/requirements.txt
RUN cat /usr/src/app/requirements.txt
RUN pip3 install -r /usr/src/app/requirements.txt
RUN python -m compileall .

COPY . /usr/src/app

EXPOSE 3000

CMD ["gunicorn", "api.controller:app", "--bind", "0.0.0.0:3000", "--log-level", "error"]
