from airflow.plugins_manager import AirflowPlugin
from airflow.models import Connection
from airflow import settings
import os

class PostgresConnectionPlugin(AirflowPlugin):
    name = "postgres_connection_plugin"

    def on_load(self):
        self.create_postgres_connection()

    def create_postgres_connection(self):
        """Ensure the `postgres_default` connection is registered."""
        session = settings.Session()

        # Get database connection parameters from environment variables
        db_user = os.getenv('ADMIN_DB_USER')
        db_password = os.getenv('ADMIN_DB_PASSWORD')
        db_host = os.getenv('DB_HOSTNAME')
        db_port = os.getenv('DB_PORT')
        db_name = os.getenv('DB_NAME')

        # Check if connection already exists
        existing_conn = session.query(Connection).filter(Connection.conn_id == 'postgres_default').first()

        if not existing_conn:
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