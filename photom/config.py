"""Configuration"""

import logging
import warnings
from importlib import import_module
from typing import TYPE_CHECKING

from dotenv import load_dotenv
from env_proxy import EnvProxy

if TYPE_CHECKING:
    from photom.store.base import Store  # pragma: no cover

logger = logging.getLogger(__name__)


class Config:
    """Configuration class for photom."""

    _singleton: "Config | None" = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super().__new__(cls)
        return cls._singleton

    def __init__(self):
        load_dotenv()

    @property
    def store_backend(self) -> str:
        """Store backend import name"""
        return EnvProxy.get_str("STORE_BACKEND") or "photom.store.sqlite.SQLiteStore"

    @property
    def store_backend_path(self) -> str:
        """Store backend path"""
        return EnvProxy.get_str("STORE_BACKEND_PATH") or ":memory:"

    def get_store_backend(self) -> "Store":
        """Get the store backend."""
        if self.store_backend == "photom.store.sqlite.SQLiteStore" and self.store_backend_path == ":memory:":
            warnings.warn("Using in-memory SQLite store. Data will not be saved.", UserWarning)

        module, cls = self.store_backend.rsplit(".", 1)
        return getattr(import_module(module), cls)(self.store_backend_path)


__all__ = ["Config"]
