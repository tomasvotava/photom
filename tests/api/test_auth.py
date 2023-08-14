"""Test authentication endpoints"""

import os
from typing import Any, Dict

import oauthlib.oauth2.rfc6749.errors
import pytest
from fastapi.testclient import TestClient
from fastapi_sso.sso.base import DiscoveryDocument, OpenID
from fastapi_sso.sso.google import GoogleSSO
from starlette.requests import Request

from photom.api.asgi import app
from photom.models import Auth


@pytest.fixture(name="client")
def client_fixture() -> TestClient:
    """Get app's test client"""
    return TestClient(app, base_url="http://photom.dev")


test_id = OpenID(id="test", email="test@example.com", display_name="Test Testowitch", provider="google")


@pytest.fixture(name="_set_env_vars")
def set_env_vars():
    """Set environment variables"""
    os.environ["GOOGLE_CLIENT_ID"] = "test_client_id"
    os.environ["GOOGLE_CLIENT_SECRET"] = "test_client_secret"


class PatchedGoogleSSO(GoogleSSO):
    """Patched GoogleSSO class"""

    @property
    def access_token(self) -> str:
        """Mock access token so that we do not rely on the network to be up for tests"""
        return "test_access_token"

    @property
    def refresh_token(self) -> str:
        """Mock refresh token so that we do not rely on the network to be up for tests"""
        return "test_refresh_token"

    async def verify_and_process(
        self,
        request: Request,
        *,
        params: Dict[str, Any] | None = None,
        headers: Dict[str, Any] | None = None,
        redirect_uri: str | None = None
    ) -> OpenID | None:
        """Mock successful response from Google SSO"""
        if request.query_params.get("code") == "success":
            return test_id
        raise oauthlib.oauth2.rfc6749.errors.AccessDeniedError()


async def discovery_document_patch(_) -> DiscoveryDocument:
    """Mock discovery document so that we do not rely on the network to be up for tests"""
    return {
        "authorization_endpoint": "http://photom.dev/oauth2/auth",
        "token_endpoint": "http://photom.dev/oauth2/token",
        "userinfo_endpoint": "http://photom.dev/oauth2/me",
    }


@pytest.fixture(name="_patch_google_sso")
def patch_google_sso(monkeypatch: pytest.MonkeyPatch):
    """Patch google sso with our test class"""
    monkeypatch.setattr("photom.api._auth.get_google_sso", lambda: PatchedGoogleSSO("client_id", "client_secret"))


class TestAuth:
    """Test suite for authentication endpoints"""

    def test_login_url(self, client: TestClient, monkeypatch: pytest.MonkeyPatch, _set_env_vars):
        """Test login url"""
        monkeypatch.setattr("fastapi_sso.sso.google.GoogleSSO.get_discovery_document", discovery_document_patch)
        response = client.get("http://photom.dev/auth/login", follow_redirects=False)
        assert response.status_code == 303
        assert response.headers["location"].startswith("http://photom.dev/oauth2/auth")

    def test_callback_url_succes(self, client: TestClient, _patch_google_sso, _set_env_vars):
        """Test login callback"""
        response = client.get("http://photom.dev/auth/callback?code=success")
        assert response.status_code == 200
        auth = Auth(**response.json())
        assert auth.openid == test_id

    def test_callback_url_failure(self, client: TestClient, _patch_google_sso, _set_env_vars):
        """Test login callback on unsuccessful response"""
        response = client.get("http://photom.dev/auth/callback?code=failure")
        assert response.status_code == 401
        assert response.json() == {"detail": "Login using Google SSO failed"}

    def test_callback_url_success_with_state(self, client: TestClient, _patch_google_sso, _set_env_vars):
        """Test login callback with state"""
        response = client.get(
            "http://photom.dev/auth/callback?code=success&state=http://photom.dev/", follow_redirects=False
        )
        assert response.status_code == 307
        assert response.headers["location"] == "http://photom.dev/"
