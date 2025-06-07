# Use official Python image
FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential libopenblas-dev liblapack-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose API port
EXPOSE 8000

# Set environment variables (optional)
ENV PYTHONUNBUFFERED=1

# Default command: start API server
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
