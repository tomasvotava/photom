"""Pydantic models"""

from fastapi_sso.sso.base import OpenID
from pydantic import BaseModel


class Auth(BaseModel):
    """Authentication data for Google APIs"""

    openid: OpenID
    access_token: str | None
    refresh_token: str
