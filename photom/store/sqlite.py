"""SQLite store backend for photom."""

import json
import logging
from contextlib import contextmanager
from sqlite3 import Connection
from types import TracebackType
from typing import Iterable, TypeVar

from photom.models import BaseModel
from photom.store.base import Store

T = TypeVar("T", bound=BaseModel)

logger = logging.getLogger(__name__)


def _find_model_in_args(*args, **kwargs) -> type[BaseModel] | None:
    """Find a model in the arguments."""
    for arg in args:
        if isinstance(arg, type) and issubclass(arg, BaseModel):
            return arg
        if isinstance(arg, BaseModel):
            return arg.__class__
    for arg in kwargs.values():
        if isinstance(arg, type) and issubclass(arg, BaseModel):
            return arg
        if isinstance(arg, BaseModel):
            return arg.__class__
    raise RuntimeError("No model found in arguments")  # pragma: no cover


def ensure_table(func):
    """A decorator for methods to make sure the table exists."""

    def wrapper(self: "SQLiteStore", *args, **kwargs):
        model = _find_model_in_args(*args, **kwargs)
        if model is not None:
            self._create_model_table(model)  # pylint: disable=protected-access
        return func(self, *args, **kwargs)

    return wrapper


class SQLiteStore(Store):
    """SQLite store backend for photom."""

    def __init__(self, database: str, **kwargs):
        """Initialize the store."""
        self._database = database
        self._conn: Connection | None = None
        self._connection_kwargs = kwargs

    def __enter__(self):
        """Enter the store context."""
        self._conn = Connection(self._database, **self._connection_kwargs)
        return self

    def __exit__(self, _exc_type: type[BaseException], _exc_val: BaseException, _exc_tb: TracebackType | None):
        """Exit the store context."""
        self._close()

    @property
    def _connection(self):
        """Get the connection."""
        if self._conn:
            return self._conn
        raise RuntimeError("Connection is not established, use with statement")

    def _close(self):
        """Close the connection."""
        if self._conn:
            self._conn.close()
            logger.info("Closed connection to database %s", self._database)

    @contextmanager
    def provide_cursor(self):
        """Provide a cursor to the store."""
        cursor = self._connection.cursor()
        yield cursor
        cursor.close()

    def _create_model_table(self, model: type[BaseModel]) -> None:
        """Create a table for a model."""
        with self.provide_cursor() as cursor:
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {model.__name__} (key TEXT PRIMARY KEY, value TEXT)")
            self._connection.commit()

    @ensure_table
    def iter_keys(self, model: type[T]) -> Iterable[str]:
        """Iterate through all keys in the store for a given model."""
        logger.debug("Listing keys for %s", model.__name__)
        with self.provide_cursor() as cursor:
            cursor.execute(f"SELECT key FROM {model.__name__}")
            yield from (row[0] for row in cursor.fetchall())

    @ensure_table
    def iter_values(self, model: type[T]) -> Iterable[T]:
        """Iterate through all values in the store for a given model."""
        logger.debug("Listing values for %s", model.__name__)
        with self.provide_cursor() as cursor:
            cursor.execute(f"SELECT value FROM {model.__name__}")
            yield from (model(**json.loads(row[0])) for row in cursor.fetchall())

    @ensure_table
    def get(self, key: str, model: type[T]) -> T | None:
        """Get a value from the store."""
        logger.debug("Getting %s from %s", key, model.__name__)
        with self.provide_cursor() as cursor:
            cursor.execute(f"SELECT value FROM {model.__name__} WHERE key=?", (key,))
            row = cursor.fetchone()
            if row is None:
                return None
            return model(**json.loads(row[0]))

    @ensure_table
    def set(self, key: str, value: BaseModel) -> None:
        """Set a value in the store."""
        logger.debug("Setting %s in %s", key, value.__class__.__name__)
        with self.provide_cursor() as cursor:
            cursor.execute(
                f"""
                INSERT INTO {value.__class__.__name__} (key, value) 
                VALUES (?, ?) 
                ON CONFLICT(key) DO UPDATE SET value=?
                """,
                (key, value.model_dump_json(), value.model_dump_json()),
            )
            self._connection.commit()

    @ensure_table
    def delete(self, key: str, model: type[T]) -> None:
        """Delete a value from the store."""
        logger.debug("Deleting %s from %s", key, model.__name__)
        with self.provide_cursor() as cursor:
            cursor.execute(f"DELETE FROM {model.__name__} WHERE key=?", (key,))
            self._connection.commit()
