FROM python:3.12

COPY requirements.txt /code/

WORKDIR /code/

RUN pip install -r requirements.txt

COPY . /code/