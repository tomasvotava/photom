"""Base for all store types. Store enables you to persist and retrieve data from the store."""

from abc import ABC, abstractmethod
from typing import TypeVar

from photom.models import BaseModel

T = TypeVar("T", bound=BaseModel)


class Store(ABC):
    """Base class for all store types."""

    @abstractmethod
    def __init__(self, **kwargs):
        """Initialize the store."""

    @abstractmethod
    def list_keys(self, model: type[T]) -> list[str]:
        """List all keys in the store for a given model."""

    @abstractmethod
    def list_values(self, model: type[T]) -> list[T]:
        """List all values in the store for a given model."""

    @abstractmethod
    def get(self, key: str, model: type[T]) -> T | None:
        """Get a value from the store."""

    @abstractmethod
    def set(self, key: str, value: BaseModel) -> None:
        """Set a value in the store."""

    @abstractmethod
    def delete(self, key: str, model: type[T]) -> None:
        """Delete a value from the store."""
