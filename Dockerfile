# syntax=docker/dockerfile:1
FROM python:3.8.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /home/manager

COPY src src
COPY .env .
COPY requirements.txt .

RUN python3 -m pip install --upgrade pip  # upgrade pip

RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD [ "python3", "src/manage.py", "runserver", "0.0.0.0:8000" ]
