"""Google SSO Auth routes"""

from fastapi import APIRouter, Request
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
            redirect_uri=request.url_for("login_callback"), state=state, params={"access_type": "offline"}
        )


@auth.get("/callback")
async def login_callback(request: Request, state: str | None = None):
    """Process login response from Google and return user info"""
    with sso:
        try:
            openid = await sso.verify_and_process(request)
        except OAuth2Error as error:
            raise photom.exceptions.NotAuthorized("Login using Google SSO failed") from error
        auth_info = Auth(openid=openid, access_token=sso.access_token, refresh_token=sso.refresh_token)
        if state:
            return RedirectResponse(url=state)
        return auth_info
