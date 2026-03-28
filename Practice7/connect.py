# connect.py
# Returns a psycopg2 connection using settings from config.py

import psycopg2
from config import DB_CONFIG


def get_connection():
    """Open and return a new database connection."""
    return psycopg2.connect(**DB_CONFIG)


def test_connection():
    """Quick connectivity check — prints PostgreSQL version."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        print("[OK] Connected to:", version)
        cur.close()
        conn.close()
    except psycopg2.OperationalError as e:
        print("[ERROR] Could not connect:", e)


if __name__ == "__main__":
    test_connection()
