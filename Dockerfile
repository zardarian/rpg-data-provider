FROM python:3.10.4-slim

LABEL RPG Data Provider

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

COPY . /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    bind9utils \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install -r requirement.txt

EXPOSE 8000

CMD [ "python", "./rpg_data_provider/manage.py","runserver", "0.0.0.0:8000"]
