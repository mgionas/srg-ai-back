# --- STAGE 1: Builder ---
FROM python:3.11-slim as builder

# Set the working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --target=/deps -r requirements.txt


# --- STAGE 2: Final production image ---
FROM python:3.11-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV PATH="/deps/bin:${PATH}"
ENV PYTHONPATH="/deps"

# Install bash
RUN apt-get update && apt-get install -y bash

# Copy dependencies
COPY --from=builder /deps /deps

# Copy application source code
COPY ./app ./app

# run server.
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000"]

