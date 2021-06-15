FROM python:3.8.5

RUN mkdir /code
COPY requirements.txt /code
COPY . /code
RUN pip install -r /code/requirements.txt
WORKDIR /code
CMD gunicorn grocery_assistant.wsgi:application --bind 0.0.0.0:8000 