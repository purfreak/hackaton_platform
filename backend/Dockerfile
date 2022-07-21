FROM python:3.10-slim

RUN apt update && apt -y install libpq-dev gcc

WORKDIR /app

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app

RUN chmod +x ./start.sh

CMD ./start.sh
