# --- STAGE 1: Builder ---
# This stage installs dependencies into a specific target directory,
# which makes them easy to copy and manage.
FROM python:3.11-slim as builder

# Set the working directory
WORKDIR /app

# Set environment variables for best practices
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies into a specific folder called /deps
# This isolates them and makes it clear what to copy later.
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --target=/deps -r requirements.txt


# --- STAGE 2: Final production image ---
FROM python:3.11-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# *** KEY FIXES ARE HERE ***
# Add the /deps/bin directory to the PATH, so executables like uvicorn can be found.
# Also set PYTHONPATH so Python can find the installed libraries.
ENV PATH="/deps/bin:${PATH}"
ENV PYTHONPATH="/deps"

# Install bash using apt-get (the correct package manager for python:slim)
RUN apt-get update && apt-get install -y --no-install-recommends bash && rm -rf /var/lib/apt/lists/*

# Copy the isolated dependencies from the builder stage
COPY --from=builder /deps /deps

# Copy your application source code (the 'app' directory)
COPY ./app ./app

# Expose the port the app will run on
EXPOSE 8000

# The command to run the Uvicorn server.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

