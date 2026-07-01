FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

ENV PORT=8080

# Shell form so Cloud Run's injected $PORT is expanded at runtime
CMD gunicorn -b 0.0.0.0:$PORT app:app
