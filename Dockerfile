# Dockerfile
FROM apache/superset

# Switch to root user to install packages and modify files
USER root

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        gcc \
        && \
    rm -rf /var/lib/apt/lists/*

# Install required Python packages
RUN pip install \
    redis \
    gevent \
    psycopg2-binary \
    flask-cors \
    sqlalchemy-bigquery \
    google-cloud-bigquery \
    pandas-gbq \
    redis \
    flask-caching \
    apache-superset[bigquery] \
    clickhouse-sqlalchemy

# Copy superset_config.py into the image
COPY superset_config.py /app/pythonpath/

# Copy entrypoint script into the image
COPY entrypoint.sh /app/

# Make entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Switch back to the 'superset' user
USER superset



# Expose port 8088
EXPOSE 8088


# Set the entrypoint to the script
ENTRYPOINT ["/app/entrypoint.sh"]
