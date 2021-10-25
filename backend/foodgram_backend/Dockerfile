FROM python:3.7.8

WORKDIR /code
COPY requirements.txt .
RUN pip install -r ./requirements.txt
COPY . /code
CMD gunicorn foodgram_backend.wsgi:application --bind 0.0.0.0:8000