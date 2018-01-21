FROM python:3-alpine

RUN apk update && apk upgrade

RUN apk add --no-cache curl python pkgconfig python-dev openssl-dev libffi-dev musl-dev make gcc

RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python

RUN mkdir -p /usr/src/project_tracker
WORKDIR /usr/src/project_tracker

COPY requirements.txt /usr/src/project_tracker/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/project_tracker

CMD export APP_SETTINGS=APP_SETTINGS
CMD export DB_PASS=DB_PASS
CMD export DB_NAME=DB_NAME
CMD export ADMIN_USER=ADMIN_USER
CMD export ADMIN_PASS=ADMIN_PASS

# Expose the Flask port
EXPOSE 5000

CMD python src/run.py