from __future__ import annotations

import sqlite3
import threading
import time
from pathlib import Path
from typing import List, Optional


class DatabaseConnectionError(Exception):
    """Raised when a database connection or pool operation fails."""


class ConnectionPool:
    def __init__(
        self,
        database_path: str,
        max_connections: int = 5,
        retry_delay: float = 1.0,
        max_retries: int = 3,
    ) -> None:
        self.database_path = Path(database_path)
        self.max_connections = max_connections
        self.retry_delay = retry_delay
        self.max_retries = max_retries
        self._lock = threading.Lock()
        self._connections: List[sqlite3.Connection] = []
        self._available: List[sqlite3.Connection] = []
        self._initialize_pool()

    def _initialize_pool(self) -> None:
        for _ in range(self.max_connections):
            connection = self._create_connection()
            self._connections.append(connection)
            self._available.append(connection)

    def _create_connection(self) -> sqlite3.Connection:
        last_error: Optional[Exception] = None
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        for attempt in range(1, self.max_retries + 1):
            try:
                connection = sqlite3.connect(str(self.database_path), check_same_thread=False)
                connection.execute("PRAGMA foreign_keys = ON")
                return connection
            except sqlite3.Error as exc:
                last_error = exc
                time.sleep(self.retry_delay)
        raise DatabaseConnectionError(
            f"Unable to create database connection after {self.max_retries} attempts."
        ) from last_error

    def acquire(self) -> sqlite3.Connection:
        with self._lock:
            if self._available:
                return self._available.pop()
            if len(self._connections) < self.max_connections:
                connection = self._create_connection()
                self._connections.append(connection)
                return connection
            raise DatabaseConnectionError("No available database connections in the pool.")

    def release(self, connection: sqlite3.Connection) -> None:
        with self._lock:
            if connection not in self._connections:
                raise DatabaseConnectionError("Connection not managed by this pool.")
            self._available.append(connection)

    def close_all(self) -> None:
        with self._lock:
            while self._connections:
                connection = self._connections.pop()
                try:
                    connection.close()
                except sqlite3.Error:
                    pass
            self._available.clear()

    def execute(self, query: str, params: tuple = (), fetch: bool = True) -> List[tuple]:
        connection = self.acquire()
        try:
            cursor = connection.execute(query, params)
            rows = cursor.fetchall() if fetch else []
            connection.commit()
            return rows
        finally:
            self.release(connection)
