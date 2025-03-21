from datetime import datetime, timedelta
import os
import pandas as pd
import boto3
from io import BytesIO
from sqlalchemy import create_engine, text
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable

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
db_name = 'companydata'

# S3 bucket
bucket_name = 'daredata-technical-challenge-data'

# Function to load monthly sales data from S3 to PostgreSQL
def load_monthly_sales_data(**kwargs):
    # Get the execution date
    execution_date = kwargs['execution_date']
    
    # Calculate previous month (since this DAG runs at the start of each month for previous month data)
    prev_month = execution_date.replace(day=1) - timedelta(days=1)
    year = prev_month.year
    month = prev_month.month
    
    # Format the date for S3 path
    date_str = f"{year}-{month:02d}-01"
    s3_key = f"sales/{date_str}/sales.csv"
    
    # Create S3 client
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
    )
    
    try:
        # Get file from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=s3_key)
        file_content = response['Body'].read()
        
        # Load data into pandas DataFrame
        df = pd.read_csv(BytesIO(file_content))
        
        # Create database connection
        engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
        
        # Create sales table if it doesn't exist
        with engine.connect() as connection:
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS sales (
                    id SERIAL PRIMARY KEY,
                    store_idx INT,
                    date DATE,
                    value NUMERIC(10, 2)
                )
            """))
            connection.commit()
        
        # Write DataFrame to PostgreSQL
        df.to_sql('sales', engine, if_exists='append', index=False)
        
        print(f"Successfully loaded sales data for {date_str}")
    except Exception as e:
        print(f"Error loading sales data for {date_str}: {str(e)}")
        raise

# Function to aggregate monthly sales
def aggregate_monthly_sales(**kwargs):
    # Get the execution date
    execution_date = kwargs['execution_date']
    
    # Calculate previous month
    prev_month = execution_date.replace(day=1) - timedelta(days=1)
    year = prev_month.year
    month = prev_month.month
    
    # Create database connection
    engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
    
    try:
        # Create monthly_sales table if it doesn't exist
        with engine.connect() as connection:
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS monthly_sales (
                    id SERIAL PRIMARY KEY,
                    store_idx INT,
                    location VARCHAR(255),
                    sale_month DATE,
                    value NUMERIC(10, 2)
                )
            """))
            connection.commit()
        
        # Query to get aggregated monthly sales data with location
        query = f"""
            SELECT s.store_idx, st.location, 
                   DATE_TRUNC('month', s.date) as sale_month,
                   SUM(s.value) as value
            FROM sales s
            JOIN stores st ON s.store_idx = st.idx
            WHERE EXTRACT(YEAR FROM s.date) = {year}
              AND EXTRACT(MONTH FROM s.date) = {month}
            GROUP BY s.store_idx, st.location, DATE_TRUNC('month', s.date)
        """
        
        # Get the monthly aggregated data
        monthly_df = pd.read_sql(query, engine)
        
        # Insert into monthly_sales table
        if not monthly_df.empty:
            # First check if the data for this month already exists
            check_query = f"""
                DELETE FROM monthly_sales 
                WHERE EXTRACT(YEAR FROM sale_month) = {year}
                  AND EXTRACT(MONTH FROM sale_month) = {month}
            """
            with engine.connect() as connection:
                connection.execute(text(check_query))
                connection.commit()
            
            # Insert the new data
            monthly_df.to_sql('monthly_sales', engine, if_exists='append', index=False)
            
        print(f"Successfully aggregated sales data for {year}-{month:02d}")
    except Exception as e:
        print(f"Error aggregating sales data for {year}-{month:02d}: {str(e)}")
        raise

# Define DAG
dag = DAG(
    'load_sales_data',
    default_args=default_args,
    description='Load and aggregate monthly sales data',
    schedule_interval='@monthly',  # Run once a month
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

# Define tasks
load_task = PythonOperator(
    task_id='load_monthly_sales',
    python_callable=load_monthly_sales_data,
    provide_context=True,
    dag=dag,
)

aggregate_task = PythonOperator(
    task_id='aggregate_monthly_sales',
    python_callable=aggregate_monthly_sales,
    provide_context=True,
    dag=dag,
)

# Set task dependencies
load_task >> aggregate_task 