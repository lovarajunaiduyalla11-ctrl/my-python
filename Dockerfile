FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# copy only what we need (small optimization)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# default port
ENV PORT=8080
EXPOSE 8080

# Use gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app", "--workers", "2"]
