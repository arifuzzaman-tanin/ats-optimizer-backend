FROM python:3.12-slim

WORKDIR /app

# curl is used by the existing container health check.
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port for container
EXPOSE 5000

# Run Flask app using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--preload", "--timeout", "30", "app:app"]
