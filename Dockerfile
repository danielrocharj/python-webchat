FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-alpine3.10

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./requirements.txt /app/requirements.txt

RUN set -eux \
    && apk add --no-cache --virtual .build-deps gcc libc-dev make \
    build-base libressl-dev libffi-dev musl-dev python3-dev \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip \
    && apk del .build-deps gcc libc-dev make

COPY ./app /app/app
