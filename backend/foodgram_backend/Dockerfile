FROM python:3.7.8

WORKDIR /code
COPY . .
RUN pip install -r requirements.txt
CMD gunicorn foodgram_backend.wsgi:application --bind 0.0.0.0:8000