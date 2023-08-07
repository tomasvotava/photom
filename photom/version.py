"""Get package's current version"""

import importlib.metadata

__version__ = importlib.metadata.version("photom")

__all__ = ["__version__"]
