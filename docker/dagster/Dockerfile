# Contains configuration for building Docker images
FROM python:3.10-slim

# Set working directory
WORKDIR /opt/dagster/app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set up Dagster home directory
ENV DAGSTER_HOME=/opt/dagster/dagster_home
RUN mkdir -p $DAGSTER_HOME

# Copy Dagster configuration
COPY docker/dagster/dagster.yaml $DAGSTER_HOME/

# Set Python path to include our code
ENV PYTHONPATH="/opt/dagster/app:${PYTHONPATH}"

# Default command
CMD ["dagster-webserver", "-h", "0.0.0.0", "-p", "3000"]