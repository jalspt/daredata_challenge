from datetime import datetime, timedelta
import os
import pandas as pd
from sqlalchemy import create_engine, text
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.sql import SqlSensor

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

# Function to create feature store
def create_feature_store():
    # Create database connection
    engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
    
    try:
        # SQL query to merge new data into the feature store
        # Using PostgreSQL's CTE for merge-like operation
        query = """
        -- First, create a temporary view with the latest data from source tables
        WITH source_data AS (
            SELECT 
                cp.idx,
                cp.attr_a,
                cp.attr_b,
                ca.scd_a,
                ca.scd_b,
                l.label
            FROM 
                customer_profiles cp
            JOIN customer_activity ca ON cp.idx = ca.idx AND ca.valid_to IS NULL
            JOIN labels l ON cp.idx = l.idx
        ),
        
        -- Records to update (exist in both source and target)
        updates AS (
            UPDATE feature_store fs
            SET 
                attr_a = sd.attr_a,
                attr_b = sd.attr_b,
                scd_a = sd.scd_a,
                scd_b = sd.scd_b,
                label = sd.label
            FROM source_data sd
            WHERE fs.idx = sd.idx
            RETURNING fs.idx
        ),
        
        -- Records to insert (exist in source but not in target)
        inserts AS (
            INSERT INTO feature_store (idx, attr_a, attr_b, scd_a, scd_b, label)
            SELECT 
                sd.idx, sd.attr_a, sd.attr_b, sd.scd_a, sd.scd_b, sd.label
            FROM source_data sd
            LEFT JOIN updates u ON sd.idx = u.idx
            WHERE u.idx IS NULL
            RETURNING idx
        )
        
        -- Delete records that exist in target but not in source
        DELETE FROM feature_store fs
        WHERE NOT EXISTS (
            SELECT 1 FROM source_data sd WHERE sd.idx = fs.idx
        );
        """
        
        # Execute the SQL query
        with engine.begin() as connection:
            connection.execute(text(query))
            # Transaction is automatically committed when the block exits
        
        print("Successfully merged data into feature_store")
    except Exception as e:
        print(f"Error merging data into feature_store: {str(e)}")
        raise

# Define sensors to check if required tables exist
def check_table_exists(table_name):
    query = f"""
    SELECT 1 FROM information_schema.tables 
    WHERE table_name = '{table_name}' 
    AND table_schema = 'public'
    """
    return query

# Define DAG
dag = DAG(
    'process_data',
    default_args=default_args,
    description='Create feature store from customer data',
    schedule_interval=None,  # No schedule - triggered by load_client_data
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

# Define sensors to wait for required tables
customer_profiles_sensor = SqlSensor(
    task_id='check_customer_profiles',
    conn_id='postgres_default',
    sql=check_table_exists('customer_profiles'),
    timeout=60 * 60,  # 1 hour timeout
    mode='poke',
    poke_interval=60,  # Check every minute
    dag=dag,
)

customer_activity_sensor = SqlSensor(
    task_id='check_customer_activity',
    conn_id='postgres_default',
    sql=check_table_exists('customer_activity'),
    timeout=60 * 60,  # 1 hour timeout
    mode='poke',
    poke_interval=60,  # Check every minute
    dag=dag,
)

labels_sensor = SqlSensor(
    task_id='check_labels',
    conn_id='postgres_default',
    sql=check_table_exists('labels'),
    timeout=60 * 60,  # 1 hour timeout
    mode='poke',
    poke_interval=60,  # Check every minute
    dag=dag,
)

# Define task to create feature store
feature_store_task = PythonOperator(
    task_id='create_feature_store',
    python_callable=create_feature_store,
    dag=dag,
)

# Set task dependencies
[customer_profiles_sensor, customer_activity_sensor, labels_sensor] >> feature_store_task 