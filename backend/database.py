import re
import os
import mysql.connector
from contextlib import contextmanager
from config import settings

_QUERIES_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "queries.sql")
_queries: dict[str, str] = {}


def _load_queries():
    '''Build dictionary mapping of query names to SQL strings'''
    with open(_QUERIES_PATH, "r") as f:
        content = f.read()
    blocks = re.split(r"--\s*name:\s*(\w+)", content)
    # blocks = [preamble, name1, body1, name2, body2, ...]
    for i in range(1, len(blocks) - 1, 2):
        name = blocks[i].strip()
        # Strip comment lines from body, keep the SQL statement
        lines = [l for l in blocks[i + 1].splitlines() if not l.strip().startswith("--")]
        _queries[name] = "\n".join(lines).strip()


_load_queries()


def query(name: str) -> str:
    '''Map query names to SQL statements'''
    return _queries[name]


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
