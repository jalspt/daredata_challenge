from airflow.plugins_manager import AirflowPlugin
from airflow.models import Connection
from airflow.hooks.base import BaseHook
from airflow import settings
import os

class PostgresConnectionPlugin(AirflowPlugin):
    name = "postgres_connection_plugin"

    def __init__(self):
        super().__init__()
        self.create_postgres_connection()
    
    def create_postgres_connection(self):
        """Create a connection to the PostgreSQL database if it doesn't exist."""
        session = settings.Session()
        
        # Get database connection parameters from environment variables
        db_user = os.environ['ADMIN_DB_USER']
        db_password = os.environ['ADMIN_DB_PASSWORD']
        db_host = os.environ['DB_HOSTNAME']
        db_port = os.environ['DB_PORT']
        db_name = os.environ['DB_NAME']
        
        # Check if connection already exists
        if not BaseHook.get_connection('postgres_default'):
            # Create new connection
            new_conn = Connection(
                conn_id='postgres_default',
                conn_type='postgres',
                host=db_host,
                login=db_user,
                password=db_password,
                schema=db_name,
                port=db_port
            )
            
            session.add(new_conn)
            session.commit()
            print("PostgreSQL connection 'postgres_default' created.")
        
        session.close() 