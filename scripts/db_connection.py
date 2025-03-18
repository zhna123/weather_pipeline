import psycopg2
import os

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
# need to set to service name if inside container
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")  # default to postgres if not set
POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)  # default to 5432 if not set

def get_db_connection():
    """
    Returns a PostgreSQL database connection using environment variables.
    """
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        port=POSTGRES_PORT
    )
    return conn
