FROM python:3.10-slim

WORKDIR /app_db

RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN pip install psycopg2-binary

COPY generate_data.py /app_db/generate_data.py
COPY python_batch_update.py /app_db/python_batch_update.py
COPY create_index_update.py /app_db/create_index_update.py
COPY temp_table.py /app_db/temp_table.py
COPY disable_triggers.py /app_db/temp_table.py

