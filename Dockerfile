FROM python:3.10-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    wget build-essential git curl && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the entire project
COPY . /app

# Set Python path
ENV PYTHONPATH=/app

# Expose port for REST API
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Launch the API server
CMD ["uvicorn", "rest_api:app", "--host", "0.0.0.0", "--port", "8080"]
