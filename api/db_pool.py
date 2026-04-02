"""
PostgreSQL connection pool for the LingoGrade API.
Uses psycopg2 pool; falls back to a stub for local dev without Postgres.
"""

import os
from contextlib import contextmanager

import psycopg2
import psycopg2.extras
from psycopg2 import pool

_pool = None


def init_pool(app=None):
    """Initialise the connection pool. Call once at startup."""
    global _pool
    dsn = os.environ.get("DATABASE_URL")
    if not dsn:
        if app:
            app.logger.warning("DATABASE_URL not set — database features disabled")
        return
    _pool = pool.ThreadedConnectionPool(
        minconn=2,
        maxconn=10,
        dsn=dsn,
    )
    if app:
        app.logger.info("PostgreSQL pool initialised")


def get_pool():
    return _pool


@contextmanager
def get_conn():
    """Yield a connection from the pool. Auto-returns on exit."""
    if _pool is None:
        raise RuntimeError("Database not configured (set DATABASE_URL)")
    conn = _pool.getconn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        _pool.putconn(conn)


@contextmanager
def get_cursor(cursor_factory=None):
    """Yield a cursor with RealDictCursor by default."""
    factory = cursor_factory or psycopg2.extras.RealDictCursor
    with get_conn() as conn:
        with conn.cursor(cursor_factory=factory) as cur:
            yield cur
