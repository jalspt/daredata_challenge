FROM apache/airflow:2.7.1

USER root
# Install additional dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        postgresql-client \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Install Python dependencies from requirements.txt
COPY ./modules/de/requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Set the Airflow web server port
ENV AIRFLOW__WEBSERVER__WEB_SERVER_PORT=8082

# Copy DAGs and plugins
COPY ./modules/de/dags /opt/airflow/dags
COPY ./modules/de/plugins /opt/airflow/plugins

# Initialize and start Airflow
CMD ["bash", "-c", "airflow db init && \
     airflow users create --username airflow --password airflow --firstname Admin --lastname User --role Admin --email admin@example.com && \
     airflow connections add 'postgres_default' --conn-type 'postgres' --conn-login \"${ADMIN_DB_USER}\" --conn-password \"${ADMIN_DB_PASSWORD}\" --conn-host \"${DB_HOSTNAME}\" --conn-port \"${DB_PORT}\" --conn-schema 'companydata' && \
     airflow scheduler & \
     airflow webserver"] 