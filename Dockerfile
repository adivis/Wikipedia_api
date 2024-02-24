FROM python:3.9.0

COPY requirements.txt /code/

WORKDIR /code/

RUN pip install -r requirements.txt

COPY . /code/
CMD [ "python3", "-m", "flask" ,"--app", "application", "run" ,"--host=0.0.0.0" ]