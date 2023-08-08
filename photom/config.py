"""Configuration"""

from dotenv import load_dotenv
from env_proxy import EnvProxy

load_dotenv()

__all__ = ["EnvProxy"]
