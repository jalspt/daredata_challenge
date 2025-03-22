FROM apache/airflow:2.7.1-python3.10

USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Install Python packages
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Create directory for environment file
RUN mkdir -p ${AIRFLOW_HOME}

# Set up Airflow configuration
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False
ENV AIRFLOW__API__AUTH_BACKENDS=airflow.api.auth.backend.basic_auth
ENV AIRFLOW__WEBSERVER__PORT=8082

# Initialize the database
ENV _AIRFLOW_DB_UPGRADE=True
ENV _AIRFLOW_WWW_USER_CREATE=True

# Create default user
ENV _AIRFLOW_WWW_USER_USERNAME=airflow
ENV _AIRFLOW_WWW_USER_PASSWORD=airflow

# Airflow scheduler configuration
ENV AIRFLOW__SCHEDULER__MIN_FILE_PROCESS_INTERVAL=10

EXPOSE 8082

# Command to run when the container starts
CMD ["bash", "-c", "airflow db init && airflow users create --username ${_AIRFLOW_WWW_USER_USERNAME} --password ${_AIRFLOW_WWW_USER_PASSWORD} --firstname Airflow --lastname Admin --role Admin --email admin@example.com && airflow webserver & airflow scheduler"] 