FROM python:3.9.0

COPY requirements.txt /code/

WORKDIR /code/

RUN pip install -r requirements.txt

COPY . /code/