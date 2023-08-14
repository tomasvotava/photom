"""Base for all store types. Store enables you to persist and retrieve data from the store."""

from abc import ABC, abstractmethod
from types import TracebackType
from typing import Iterable, Type, TypeVar

from photom.models import BaseModel

T = TypeVar("T", bound=BaseModel)


class Store(ABC):
    """Base class for all store types."""

    @abstractmethod
    def __init__(self, **kwargs):
        """Initialize the store."""

    @abstractmethod
    def __enter__(self) -> "Store":
        """Enter the store context."""

    @abstractmethod
    def __exit__(self, _exc_type: Type[BaseException], _exc_val: BaseException, _exc_tb: TracebackType | None):
        """Exit the store context."""

    @abstractmethod
    def iter_keys(self, model: type[T]) -> Iterable[str]:
        """Iterate through all keys in the store for a given model."""

    @abstractmethod
    def iter_values(self, model: type[T]) -> Iterable[T]:
        """Iterate through all values in the store for a given model."""

    @abstractmethod
    def get(self, key: str, model: type[T]) -> T | None:
        """Get a value from the store."""

    @abstractmethod
    def set(self, key: str, value: BaseModel) -> None:
        """Set a value in the store."""

    @abstractmethod
    def delete(self, key: str, model: type[T]) -> None:
        """Delete a value from the store."""
