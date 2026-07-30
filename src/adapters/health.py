from __future__ import annotations

from .db import ConnectionPool, DatabaseConnectionError


def database_health_status(pool: ConnectionPool) -> bool:
    """Check the health of the configured database connection pool."""
    try:
        pool.execute("SELECT 1;", fetch=True)
        return True
    except DatabaseConnectionError:
        return False
