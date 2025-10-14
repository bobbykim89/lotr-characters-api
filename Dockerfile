# Use a slim python image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system deps required to build some Python packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
       gcc \
       curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (caches layer)
COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt

# Copy app code
COPY . .

# Ensure entrypoint is executable
RUN chmod +x ./entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./docker_entrypoint.sh"]