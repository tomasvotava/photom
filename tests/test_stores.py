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
        # TODO add test for when there are keys
        assert not list(store.iter_keys(test_model.__class__))

    def test_iter_values(self, store: Store, test_model: BaseModel):
        """Test iter_values."""
        # TODO add test for when there are values
        assert not list(store.iter_values(test_model.__class__))

    def test_get(self, store: Store, test_model: BaseModel):
        """Test get."""
        assert store.get("test", test_model.__class__) is None

    def test_set(self, store: Store, test_model: BaseModel):
        """Test set."""
        store.set("test", test_model)
        assert set(store.iter_keys(test_model.__class__)) == {"test"}
        assert store.get("test", test_model.__class__) == test_model

    def test_delete(self, store: Store, test_model: BaseModel):
        """Test delete."""
        store.set("test", value=test_model)
        assert store.get("test", test_model.__class__) == test_model
        store.delete("test", model=test_model.__class__)
        assert store.get("test", test_model.__class__) is None
