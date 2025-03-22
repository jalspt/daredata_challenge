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
        # SQL query to create the feature store
        # Joining customer profiles, latest customer activity, and labels
        query = """
        CREATE TABLE IF NOT EXISTS feature_store AS
        SELECT 
            cp.idx,
            cp.attr_a,
            cp.attr_b,
            ca.scd_a,
            ca.scd_b,
            l.label
        FROM 
            customer_profiles cp
        JOIN (
            -- Get only the latest activity for each customer (where valid_to is NULL)
            SELECT * FROM customer_activity 
            WHERE valid_to IS NULL
        ) ca ON cp.idx = ca.idx
        JOIN labels l ON cp.idx = l.idx;
        
        -- Grant permissions to DS and MLE users
        GRANT SELECT ON feature_store TO ds_user_role;
        GRANT ALL PRIVILEGES ON feature_store TO mle_user_role;
        """
        
        # Execute the SQL query
        with engine.connect() as connection:
            connection.execute(text("DROP TABLE IF EXISTS feature_store"))
            connection.execute(text(query))
            connection.commit()
        
        print("Successfully created feature_store table")
    except Exception as e:
        print(f"Error creating feature_store: {str(e)}")
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
    schedule_interval=None,  # Triggered manually after client data and sales data are loaded
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