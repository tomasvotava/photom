"""SQLite store backend for photom."""

import json
import logging
from sqlite3 import Connection, connect
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
        self._conn: Connection = connect(database, **kwargs)

    def _create_model_table(self, model: type[BaseModel]) -> None:
        """Create a table for a model."""
        cursor = self._conn.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {model.__name__} (key TEXT PRIMARY KEY, value TEXT)")
        self._conn.commit()

    @ensure_table
    def iter_keys(self, model: type[T]) -> Iterable[str]:
        """Iterate through all keys in the store for a given model."""
        logger.debug("Listing keys for %s", model.__name__)
        cursor = self._conn.cursor()
        cursor.execute(f"SELECT key FROM {model.__name__}")
        yield from (row[0] for row in cursor.fetchall())

    @ensure_table
    def iter_values(self, model: type[T]) -> Iterable[T]:
        """Iterate through all values in the store for a given model."""
        logger.debug("Listing values for %s", model.__name__)
        cursor = self._conn.cursor()
        cursor.execute(f"SELECT value FROM {model.__name__}")
        yield from (model(**json.loads(row[0])) for row in cursor.fetchall())

    @ensure_table
    def get(self, key: str, model: type[T]) -> T | None:
        """Get a value from the store."""
        logger.debug("Getting %s from %s", key, model.__name__)
        cursor = self._conn.cursor()
        cursor.execute(f"SELECT value FROM {model.__name__} WHERE key=?", (key,))
        row = cursor.fetchone()
        if row is None:
            return None
        return model(**json.loads(row[0]))

    @ensure_table
    def set(self, key: str, value: BaseModel) -> None:
        """Set a value in the store."""
        logger.debug("Setting %s in %s", key, value.__class__.__name__)
        cursor = self._conn.cursor()
        cursor.execute(
            f"INSERT INTO {value.__class__.__name__} (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value=?",
            (key, value.model_dump_json(), value.model_dump_json()),
        )
        self._conn.commit()

    @ensure_table
    def delete(self, key: str, model: type[T]) -> None:
        """Delete a value from the store."""
        logger.debug("Deleting %s from %s", key, model.__name__)
        cursor = self._conn.cursor()
        cursor.execute(f"DELETE FROM {model.__name__} WHERE key=?", (key,))
        self._conn.commit()
