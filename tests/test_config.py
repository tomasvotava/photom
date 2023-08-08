"""Test photom.config module"""

import os
from pathlib import Path

import pytest

from photom.config import Config


class TestConfig:
    """Config test suite"""

    def test_unset_store(self):
        """Test unset store"""
        config = Config()
        with pytest.warns(UserWarning, match="Using in-memory SQLite store. Data will not be saved."):
            config.get_store_backend()

        assert config.store_backend_path == ":memory:", "Default store backend path is not :memory:"
        assert config.store_backend == "photom.store.sqlite.SQLiteStore", "Default store backend is not SQLiteStore"

    def test_singleton(self):
        """Test singleton"""
        assert Config() is Config(), "Config is not a singleton"

    @pytest.mark.parametrize("store", ["photom.store.sqlite.SQLiteStore", "photom.store.file.FileStore"])
    def test_set_store(self, store: str, tmp_path: Path):
        """Test set store"""
        store_path = (
            os.path.join(tmp_path, "test.db") if store == "photom.store.sqlite.SQLiteStore" else str(tmp_path.resolve())
        )
        os.environ["STORE_BACKEND"] = store
        os.environ["STORE_BACKEND_PATH"] = store_path

        config = Config()
        assert config.store_backend_path == store_path
        assert config.store_backend == store
        assert config.get_store_backend().__class__.__name__ == store.split(".")[-1]
