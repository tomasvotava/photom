"""File store implementation.
This store stores stored data in a directory structure. Each model has a subdirectory, each model's key is a file in
that subdirectory. The file contains the JSON representation of the model."""


import json
import logging
import os
from typing import Any, TypeVar

from photom.models import BaseModel
from photom.store.base import Store

T = TypeVar("T", bound=BaseModel)

logger = logging.getLogger(__name__)


def _nonone(values: list[Any | None]) -> list[Any]:
    """Return a list of non-None values."""
    return [value for value in values if value is not None]


class FileStore(Store):
    """File store backend for photom."""

    def __init__(self, directory: str, **kwargs):
        """Initialize the store."""
        self._directory = os.path.abspath(directory)
        os.makedirs(self._directory, exist_ok=True)

    def _get_key(self, key: str, model_or_instance: BaseModel | type[BaseModel]) -> str:
        """Get the key to use for the store."""
        if isinstance(model_or_instance, BaseModel):
            keyhint = model_or_instance.__class__.__name__
        else:
            keyhint = model_or_instance.__name__
        return os.path.join(self._directory, keyhint, key)

    def list_keys(self, model: type[T]) -> list[str]:
        """List all keys in the store for a given model."""
        model_dir = os.path.join(self._directory, model.__name__)
        if not os.path.isdir(model_dir):
            return []
        return os.listdir(model_dir)

    def list_values(self, model: type[T]) -> list[T]:
        """List all values in the store for a given model."""
        return _nonone([self.get(key, model) for key in self.list_keys(model)])

    def get(self, key: str, model: type[T]) -> T | None:
        """Get a value from the store."""
        key = self._get_key(key, model)
        if not os.path.isfile(key):
            return None
        with open(key, "r", encoding="utf-8") as file:
            return model(**json.load(file))

    def set(self, key: str, value: BaseModel) -> None:
        """Set a value in the store."""
        key = self._get_key(key, value)
        os.makedirs(os.path.dirname(key), exist_ok=True)
        with open(key, "w", encoding="utf-8") as file:
            json.dump(value.dict(), file)

    def delete(self, key: str, model: type[T]) -> None:
        """Delete a value from the store."""
        key = self._get_key(key, model)
        if os.path.isfile(key):
            os.remove(key)
