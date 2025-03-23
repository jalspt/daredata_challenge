# Technical Assessment Solution

## Project Overview

This document describes my implementation of the technical assessment, which involves building a complete system with data engineering, data science, machine learning and deployment components.

## Implemented Modules

### Data Engineering Module

## Overview

This module implements a data engineering solution for processing and storing client data. It includes:

1. A PostgreSQL database with user roles and permissions
2. An Airflow instance for workflow orchestration
3. ETL pipelines to process data from S3 and create a feature store

#### PostgreSQL Database

- Database name: `companydata`
- Admin user with full access
- DS user with read-only access
- MLE user with full access to the public schema
- Created initialization scripts in the `db_admin` directory

#### Airflow for Workflow Orchestration

- Deployed Airflow UI accessible at port 8082
- Configured with username `airflow` and password `airflow`
- Set up to load custom DAGs from the `dags` directory
- Connected to PostgreSQL for workflow state management
- Configured with access to S3 for data ingestion

#### ETL Workflows Implementation

Implemented three main Airflow DAGs:

1. `load_client_data` - One-off workflow that loads customer profiles, activity data, and labels from S3
2. `load_sales_data` - Monthly workflow that loads and aggregates sales data
3. `process_data` - Creates the feature store by joining customer data tables

#### Directory Structure

- `dags/` - Contains Airflow DAGs for data processing
- `docker/` - Dockerfile and requirements for Airflow
- `plugins/` - Custom Airflow plugins and helpers
- `db_admin/` - Database initialization scripts

## Data Storage

PostgreSQL data is stored locally in the module's directory structure:

- PostgreSQL data: `modules/de/data/postgres/`

### Data Science Module Task

I implemented the "Add a new function to the `data_science` package to fetch the data from the sales table" task:

- Added a `get_sales_data()` function to the `fetch_data.py` file
- The function connects to the database and retrieves all sales data
- Used the existing connection string pattern for consistency
- Verified the function works by testing it from the command line

### Machine Learning Engineering Module Task

I implemented the "Add logging to the `MLEModel` class" task:

- Added Python's logging module to the MLEModel class
- Configured logging with appropriate format and level
- Added log entries to all key methods (load, save, fit, predict)
- Enhanced error handling in the log_to_storage method
- Log messages include relevant information (args, shapes, client ids)

## Deployment Module (To Be Completed)

### CI/CD Implementation

For the deployment module, I implemented a CI/CD pipeline using GitHub Actions to ensure code quality:

- Created a GitHub Actions workflow that runs automatically on pull request to main branch
- Implemented automatic code formatting with Black to ensure consistent code style
- Set up automatic commit of formatted code back to the repository
- Ensured proper repository permissions for GitHub Actions

This CI/CD implementation helps maintain code quality by enforcing a consistent code style across the project, which will be critical when implementing the full API and deployment infrastructure.

### API Implementation

I've implemented a simple Flask-based API that serves model predictions through HTTP:

- Created a RESTful API endpoint at `/predict` that accepts POST requests
- Implemented proper model loading from the DS module's models directory
- Added input validation and error handling to ensure robust operation
- Configured the server to be internet-accessible (running on 0.0.0.0)
- Structured the API to return prediction labels in JSON format

The API provides everything needed for end-users to make HTTP requests and receive label predictions for new clients. Key features include:

- **Dynamic model loading**: API automatically locates and loads the trained model
- **Input validation**: Validates incoming requests to ensure required fields are present
- **Error handling**: Gracefully handles exceptions and returns appropriate HTTP status codes
- **JSON responses**: Returns predictions in a standardized JSON format
- **Production-ready configuration**: Configured for deployment with proper host binding

The implementation follows best practices for Flask API development and ensures the model is properly integrated with the web service.

### Architecture Design

_[Describe the cloud architecture here]_

### Testing and Monitoring

_[Describe testing and monitoring setup here]_

## Running the Project

### Setup and Starting Services

The project is configured to run as part of the docker-compose setup. Start all services with:

```bash
# Start all services in detached mode
docker-compose up -d
```

### Testing the Data Engineering Module

#### 1. Verify PostgreSQL Database

Confirm that the PostgreSQL database is running and properly configured:

```bash
# Connect to PostgreSQL using the admin user
docker exec -it postgres psql -U admin -d companydata

# List all tables in the public schema
\dt public.*

# Verify user roles and permissions
\du

# Check if the database is properly initialized
SELECT COUNT(*) FROM public.clients;
SELECT COUNT(*) FROM public.activity;
SELECT COUNT(*) FROM public.labels;
SELECT COUNT(*) FROM public.sales;

# Exit PostgreSQL
\q
```

#### 2. Access Airflow UI

Access the Airflow UI to check and trigger workflows:

- Open your browser and navigate to `http://localhost:8082`
- Login with username `airflow` and password `airflow`
- Verify that all DAGs are listed in the UI:
  - `load_client_data`
  - `load_sales_data`
  - `process_data`

#### 3. Run ETL Workflows

Execute the workflows in the proper order:

```bash
# Trigger the client data load (one-time setup)
docker exec -it airflow airflow dags trigger load_client_data

# Wait for completion, then trigger the sales data load
docker exec -it airflow airflow dags trigger load_sales_data

# Finally, trigger the data processing pipeline
docker exec -it airflow airflow dags trigger process_data
```

Alternatively, you can trigger these DAGs from the Airflow UI:

1. Navigate to the DAGs list
2. Click the "Play" button next to each DAG
3. Monitor execution in the "Graph View"

#### 4. Verify Data Processing Results

Check that the feature store was properly created:

```bash
# Connect to PostgreSQL
docker exec -it postgres psql -U admin -d companydata

# Check the feature store table
SELECT COUNT(*) FROM public.feature_store;

# Verify that client profiles, activities, and sales data are joined correctly
SELECT * FROM public.feature_store LIMIT 5;

# Exit PostgreSQL
\q
```

#### 5. Test Data Access with Different Users

Verify that user permissions are correctly set:

```bash
# Connect as DS user (read-only)
docker exec -it postgres psql -U ds_user -d companydata

# Attempt to read data (should succeed)
SELECT * FROM public.feature_store LIMIT 5;

# Attempt to modify data (should fail)
INSERT INTO public.clients VALUES (999, 'Test Client', 'test@example.com');

# Exit and connect as MLE user
\q
docker exec -it postgres psql -U mle_user -d companydata

# MLE user should have read and write access
SELECT * FROM public.feature_store LIMIT 5;
INSERT INTO public.test_table VALUES (1, 'Test Value');
```

## Implementation Timeline

### Phase 1: Setup & Environment Configuration

- [Date] Initial review of requirements
- [Date] Set up local development environment
- [Date] Configured Docker and environment variables

### Phase 2: Data Engineering Module

- [Date] Database schema and user setup
- [Date] Airflow configuration
- [Date] ETL workflows implementation
- [Date] Testing and validation

### Phase 3: Module Tasks

- [Date] Implemented DS module task: Added get_sales_data() function
- [Date] Implemented MLE module task: Added logging to MLEModel class
- [Date] Implemented CI/CD with GitHub Actions for code formatting

### Phase 4: Deployment Module

- [To be completed]

### Phase 5: Documentation & Submission

- [Date] Created SOLUTION.md structure
- [To be completed]

## Design Decisions and Challenges

### Design Decisions

_[Document key design decisions here, such as:]_

- Why certain tools or approaches were chosen
- Architecture considerations
- Security measures
- Performance optimizations
- **CI/CD Approach**: Chose GitHub Actions for CI/CD due to its tight integration with GitHub repositories, ease of setup, and ability to automate code quality tasks with minimal configuration.

### Challenges Faced

_[Document challenges you encountered and how you resolved them:]_

- Any technical obstacles
- Integration issues
- Performance considerations
- **GitHub Actions Permissions**: Initially encountered permission issues with GitHub Actions when trying to commit formatted code back to the repository. Resolved by configuring proper workflow permissions in the repository settings.

## Screenshots and Evidence

_[This section will include screenshots of the deployed system, API in action, etc.]_
