#FROM alpine:3.7
#FROM python:3
FROM python:3.7-rc-alpine

LABEL maintainer="Vitaly Panyukhin <creatiwww@yandex.ru>"

# requered to let connections to postgres work through sqlalchemy
RUN apk update && apk add --no-cache build-base postgresql-dev

# requered to instal on pure alpine python and pip
#RUN apk add --no-cache \
#    python3 && \
#    python3 -m ensurepip && \
#    rm -r /usr/lib/python*/ensurepip && \
#    pip3 install --upgrade pip setuptools && \
#    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
#    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
#    rm -r /root/.cache

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

CMD ["gunicorn", "main:app", "-b", "0.0.0.0:5000"]