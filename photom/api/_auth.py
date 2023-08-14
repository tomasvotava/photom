"""Google SSO Auth routes"""

from fastapi import APIRouter, Request, Response, status
from fastapi.responses import RedirectResponse
from fastapi_sso.sso.google import GoogleSSO
from oauthlib.oauth2.rfc6749.errors import OAuth2Error

import photom.exceptions
from photom.config import Config
from photom.models import Auth

config = Config()

auth = APIRouter(prefix="/auth", tags=["auth"])

sso = GoogleSSO(
    client_id=config.google_client_id,
    client_secret=config.google_client_secret,
    allow_insecure_http=config.oauthlib_insecure_transport,
    scope=[
        "openid",
        "email",
        "profile",
        "https://www.googleapis.com/auth/photoslibrary",
        "https://www.googleapis.com/auth/drive",
    ],
)


@auth.get("/login")
async def login(request: Request, state: str | None = None):
    """Redirect to Google login page"""
    with sso:
        return await sso.get_login_redirect(
            redirect_uri=request.url_for("login_callback"),
            state=state,
            params={"access_type": "offline", "prompt": "select_account"},
        )


@auth.get("/callback", response_model=Auth)
async def login_callback(request: Request, state: str | None = None) -> Auth | RedirectResponse:
    """Process login response from Google and return user info"""
    with sso:
        try:
            openid = await sso.verify_and_process(request)
        except OAuth2Error as error:
            raise photom.exceptions.NotAuthorized("Login using Google SSO failed") from error
        auth_info = Auth(openid=openid, access_token=sso.access_token, refresh_token=sso.refresh_token)
        with config.get_store_backend() as store:
            store.set(auth_info.openid.email, auth_info)
        if state:
            return RedirectResponse(url=state)
        return auth_info


@auth.get("/")
async def list_accounts() -> list[Auth]:
    """List all logins currently present in the store"""
    with config.get_store_backend() as store:
        return list(store.iter_values(Auth))


@auth.delete("/{email}")
async def delete_account(email: str):
    """Delete a stored login identified by its email address"""
    with config.get_store_backend() as store:
        store.delete(email, Auth)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
