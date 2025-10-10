FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENC PYTHONUNBUFFERED=1

CMD["gunicorn", "--bind", "0.0.0.0:8000", "crop_price_tracker.wsgi:application"]
