import mysql.connector
from contextlib import contextmanager
from config import settings


@contextmanager
def get_db():
    conn = mysql.connector.connect(
        host=settings.db_host,
        user=settings.db_user,
        password=settings.db_password,
        database=settings.db_name,
    )
    try:
        yield conn
    finally:
        conn.close()
