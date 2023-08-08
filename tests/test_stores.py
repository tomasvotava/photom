"""Test sqlite store."""

import pytest
from fastapi_sso.sso.base import OpenID

from photom.models import Auth, BaseModel
from photom.store.base import Store
from photom.store.file import FileStore
from photom.store.sqlite import SQLiteStore

test_models = [
    Auth(
        openid=OpenID(id="test", email="test@example.com", display_name="Test Testowitch"),
        access_token="supersecret_access_token",
        refresh_token="megasecret_ultratoken",
    )
]

stores = [SQLiteStore(":memory:"), FileStore("./tmp")]
pytestmark = [pytest.mark.parametrize("test_model", test_models), pytest.mark.parametrize("store", stores)]


class TestStores:
    """Test stores."""

    def test_list_keys(self, store: Store, test_model: BaseModel):
        """Test list_keys."""
        assert store.list_keys(test_model.__class__) == []

    def test_list_values(self, store: Store, test_model: BaseModel):
        """Test list_values."""
        assert store.list_values(test_model.__class__) == []

    def test_get(self, store: Store, test_model: BaseModel):
        """Test get."""
        assert store.get("test", test_model.__class__) is None

    def test_set(self, store: Store, test_model: BaseModel):
        """Test set."""
        store.set("test", test_model)
        assert store.list_keys(test_model.__class__) == ["test"]
        assert store.get("test", test_model.__class__) == test_model

    def test_delete(self, store: Store, test_model: BaseModel):
        """Test delete."""
        store.set("test", value=test_model)
        assert store.get("test", test_model.__class__) == test_model
        store.delete("test", model=test_model.__class__)
        assert store.get("test", test_model.__class__) is None
