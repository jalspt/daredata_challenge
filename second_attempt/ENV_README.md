# Environment Configuration

This project uses a `.env` file to manage environment variables. This approach provides several benefits:

1. **Separation of Configuration**: Keeps sensitive information separate from code
2. **Centralized Management**: Single place to configure all environment variables
3. **Security**: Prevents secrets from being committed to version control
4. **Consistency**: Same variables are used across different containers

## Environment Variables

The `.env` file contains the following variables:

### Database Configuration

- `DB_HOSTNAME`: Hostname for the database server
- `DB_PORT`: Port for the database server
- `DB_NAME`: Name of the database
- `ADMIN_DB_USER`: Admin username for the database
- `ADMIN_DB_PASSWORD`: Admin password for the database
- `DS_DB_PASSWORD`: Password for the data science user
- `MLE_DB_PASSWORD`: Password for the machine learning engineer user

### Airflow Configuration

- `AIRFLOW_HOME`: Home directory for Airflow
- `AIRFLOW_WWW_USER`: Username for Airflow web UI
- `AIRFLOW_WWW_PASSWORD`: Password for Airflow web UI

### AWS Configuration

- `AWS_ACCESS_KEY_ID`: AWS access key ID
- `AWS_SECRET_ACCESS_KEY`: AWS secret access key
- `AWS_DEFAULT_REGION`: Default AWS region
- `S3_BUCKET_NAME`: Name of the S3 bucket containing the data

## Setup Instructions

1. Copy the `.env.example` file to `.env`
2. Fill in the required values
3. Make sure `.env` is ignored in your version control system

**IMPORTANT**: Never commit the `.env` file with real values to version control. Add it to your `.gitignore` file.
