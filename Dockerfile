# syntax = docker/dockerfile:1.4

FROM python:3.13.5-alpine3.22

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

EXPOSE 8000

cmd ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]