FROM python:3.8-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /stock_robot/

COPY ./stockrobot-requirements.txt /stock_robot/requirements.txt

RUN set -eux \
    && apk add --no-cache --virtual .build-deps gcc libc-dev make \
    build-base libressl-dev libffi-dev musl-dev python3-dev \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r /stock_robot/requirements.txt \
    && rm -rf /root/.cache/pip \
    && apk del .build-deps gcc libc-dev make

COPY ./stock_robot /stock_robot
WORKDIR /stock_robot/
