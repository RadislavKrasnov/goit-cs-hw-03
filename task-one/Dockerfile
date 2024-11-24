FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.11 python3.11-venv python3.11-distutils  python3.11-dev && \
    apt-get -y install libpq-dev gcc && \
    apt-get clean

RUN ln -s /usr/bin/python3.11 /usr/bin/python

WORKDIR /app

RUN apt-get install -y curl
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11
RUN pip install psycopg2 Faker

CMD ["python"]
