
import psycopg2
from conf import load_configs
from contextlib import contextmanager

@contextmanager
def create_connection():
    configs = load_configs()
    conn = psycopg2.connect(
        host=configs['host'],
        port=configs['port'],
        database=configs['database'],
        user=configs['user'],
        password=configs['password'],
    )
    yield conn
    conn.rollback()
    conn.close()
