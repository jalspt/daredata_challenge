# Data Engineering Module

## Overview

This module implements a data engineering solution for processing and storing client data. It includes:

1. A PostgreSQL database with user roles and permissions
2. An Airflow instance for workflow orchestration
3. ETL pipelines to process data from S3 and create a feature store

## Components

### PostgreSQL Database

The database is configured with:

- Database name: `companydata`
- Admin user with full access
- DS user with read-only access
- MLE user with full access to the public schema

### Airflow

Airflow is configured to:

- Run on port 8082
- Load custom DAGs from the `dags` directory
- Connect to PostgreSQL for workflow orchestration
- Access S3 for data ingestion

## Running the Module

The module is configured to run as part of the docker-compose setup. You can start it with:

```bash
docker-compose up -d
```

Then access the Airflow UI at `http://localhost:8082` (username: `airflow`, password: `airflow`).

## Workflows

The module includes the following Airflow DAGs:

1. `load_client_data` - One-off workflow to load customer profiles, activity data, and labels
2. `load_sales_data` - Monthly workflow to load and aggregate sales data
3. `process_data` - Creates the feature store by joining customer data

## Directory Structure

- `dags/` - Airflow DAGs for data processing
- `docker/` - Dockerfile and requirements for Airflow
- `plugins/` - Custom Airflow plugins and helpers
- `db_admin/` - Database initialization scripts
- `data/postgres/` - Persistent storage for PostgreSQL data
- `logs/` - Airflow logs storage

## Data Storage

Both PostgreSQL data and Airflow logs are stored locally in the module's directory structure:

- PostgreSQL data: `modules/de/data/postgres/`
- Airflow logs: `modules/de/logs/`

This provides easy access to the data for development and debugging purposes. Make sure these directories are excluded from version control (but keep the empty directories).
