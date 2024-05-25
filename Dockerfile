FROM python:3.10.6-slim-buster

RUN apt-get update && apt-get install -y libpq-dev gcc

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt requirements.txt 

RUN pip install -r requirements.txt

COPY . .

RUN python manage.py makemigrations && python manage.py migrate

EXPOSE 8000

CMD [ "python" ,"manage.py" ,"runserver" ,"0.0.0.0:8000" ]

