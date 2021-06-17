FROM python:3.8.5

WORKDIR /code
COPY requirements.txt .
COPY . .
RUN pip install -r requirements.txt
CMD gunicorn grocery_assistant.wsgi:application --bind 0.0.0.0:8000 