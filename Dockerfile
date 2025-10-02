# --- STAGE 1: Base image with dependencies ---
FROM python:3.11-slim as base

# Set the working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Upgrade pip and install the Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


# --- STAGE 2: Final production image ---
FROM python:3.11-slim

WORKDIR /app

# Copy the installed dependencies from the 'base' stage
COPY --from=base /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# *** ADDED THIS LINE TO FIX THE ERROR ***
COPY --from=base /usr/local/bin /usr/local/bin

# Copy your application source code (the 'app' directory)
COPY ./app ./app


# run the Uvicorn server.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]