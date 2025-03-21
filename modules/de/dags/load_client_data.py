from datetime import datetime, timedelta
import os
import pandas as pd
import boto3
from botocore import UNSIGNED
from botocore.client import Config
from io import BytesIO
from sqlalchemy import create_engine
from airflow import DAG
from airflow.operators.python import PythonOperator

# Default arguments for DAG
default_args = {
    'owner': 'de_team',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Database connection parameters
db_user = os.environ['ADMIN_DB_USER']
db_password = os.environ['ADMIN_DB_PASSWORD']
db_host = os.environ['DB_HOSTNAME']
db_port = os.environ['DB_PORT']
db_name = os.environ['DB_NAME']

# S3 bucket
bucket_name = 'daredata-technical-challenge-data'

# Function to load data from S3 to PostgreSQL
def load_data_from_s3_to_postgres(file_name, table_name, **kwargs):
    # Create S3 client
    s3_client = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    
    try:
        # Get file from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
        file_content = response['Body'].read()
        
        # Load data into pandas DataFrame
        df = pd.read_csv(BytesIO(file_content))
        
        # Create database connection
        engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
        
        # Write DataFrame to PostgreSQL
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        
        print(f"Successfully loaded {file_name} to {table_name} table")
    except Exception as e:
        print(f"Error loading {file_name}: {str(e)}")
        raise
    
# Define DAG
dag = DAG(
    'load_client_data',
    default_args=default_args,
    description='Load customer data from S3 to PostgreSQL',
    schedule_interval=None,  # One-off workflow, triggered manually
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

# Define tasks
customer_profiles_task = PythonOperator(
    task_id='load_customer_profiles',
    python_callable=load_data_from_s3_to_postgres,
    op_kwargs={
        'file_name': 'customer_profiles.csv',
        'table_name': 'customer_profiles'
    },
    dag=dag,
)

customer_activity_task = PythonOperator(
    task_id='load_customer_activity',
    python_callable=load_data_from_s3_to_postgres,
    op_kwargs={
        'file_name': 'customer_activity.csv',
        'table_name': 'customer_activity'
    },
    dag=dag,
)

labels_task = PythonOperator(
    task_id='load_labels',
    python_callable=load_data_from_s3_to_postgres,
    op_kwargs={
        'file_name': 'labels.csv',
        'table_name': 'labels'
    },
    dag=dag,
)

stores_task = PythonOperator(
    task_id='load_stores',
    python_callable=load_data_from_s3_to_postgres,
    op_kwargs={
        'file_name': 'stores.csv',
        'table_name': 'stores'
    },
    dag=dag,
)

# Set task dependencies (run in parallel since they're independent)
# No specific dependencies required, tasks can run in parallel 