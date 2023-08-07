"""Test the version of the package."""

from photom.version import __version__


def test_version():
    """Test the version of the package."""
    assert __version__ > "0.0.0", "Version should be higher than 0.0.0"
