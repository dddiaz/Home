FROM python:3

MAINTAINER Daniel Diaz "daniel.delvin.diaz+dockerfile@gmail.com"

EXPOSE 5000

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

CMD python home.py