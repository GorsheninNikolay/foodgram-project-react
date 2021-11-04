FROM python:3.7.8

WORKDIR /code
COPY requirements.txt .
COPY data .
RUN pip install -r ./requirements.txt
COPY . /code