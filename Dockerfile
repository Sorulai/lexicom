FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", ":8000", "--workers", "1", "app.main:app", "--worker-class", "uvicorn.workers.UvicornWorker", "--preload", "--timeout", "120"]