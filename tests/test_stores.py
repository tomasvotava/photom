"""Test sqlite store."""

import os
import shutil
from tempfile import gettempdir

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

test_tempdir = os.path.join(gettempdir(), "photom_test")

stores = [SQLiteStore(":memory:"), FileStore(test_tempdir)]
pytestmark = [pytest.mark.parametrize("test_model", test_models), pytest.mark.parametrize("store", stores)]


@pytest.fixture(autouse=True)
def prepare_and_cleanup():
    """Prepare and cleanup after tests."""
    if os.path.exists(test_tempdir):
        shutil.rmtree(test_tempdir)
    yield
    if os.path.exists(test_tempdir):
        shutil.rmtree(test_tempdir)


class TestStores:
    """Test stores."""

    def test_iter_keys(self, store: Store, test_model: BaseModel):
        """Test iter_keys."""
        with store:
            assert not list(store.iter_keys(test_model.__class__))
            store.set("test", value=test_model)
            store.set("test2", value=test_model)
            assert set(store.iter_keys(test_model.__class__)) == {"test", "test2"}

    def test_iter_values(self, store: Store, test_model: BaseModel):
        """Test iter_values."""
        with store:
            assert not list(store.iter_values(test_model.__class__))
            store.set("test", value=test_model)
            store.set("test2", value=test_model)
            assert set(store.iter_values(test_model.__class__)) == {test_model, test_model}

    def test_get(self, store: Store, test_model: BaseModel):
        """Test get."""
        with store:
            assert store.get("test", test_model.__class__) is None
            store.set("test", value=test_model)
            assert store.get("test", test_model.__class__) == test_model

    def test_set(self, store: Store, test_model: BaseModel):
        """Test set."""
        with store:
            store.set("test", test_model)
            assert set(store.iter_keys(test_model.__class__)) == {"test"}
            assert store.get("test", test_model.__class__) == test_model

    def test_delete(self, store: Store, test_model: BaseModel):
        """Test delete."""
        with store:
            store.set("test", value=test_model)
            assert store.get("test", test_model.__class__) == test_model
            store.delete("test", model=test_model.__class__)
            assert store.get("test", test_model.__class__) is None
