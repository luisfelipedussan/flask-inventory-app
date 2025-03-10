# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory for application
WORKDIR /app

# Install system dependencies required for MySQL and networking
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    curl \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set Flask environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

# Expose port 5000 for Flask application
EXPOSE 5000

# Start Flask development server
CMD ["flask", "run", "--host=0.0.0.0"] 