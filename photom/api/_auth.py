"""Google SSO Auth routes"""

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi_sso.sso.google import GoogleSSO

from photom.config import EnvProxy
from photom.models import Auth

auth = APIRouter(prefix="/auth", tags=["auth"])

sso = GoogleSSO(
    client_id=EnvProxy.get_str_strict("GOOGLE_CLIENT_ID"),
    client_secret=EnvProxy.get_str_strict("GOOGLE_CLIENT_SECRET"),
    allow_insecure_http=bool(EnvProxy.get_int("OAUTHLIB_INSECURE_TRANSPORT")),
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
        openid = await sso.verify_and_process(request)
        auth_info = Auth(openid=openid, access_token=sso.access_token, refresh_token=sso.refresh_token)
        if state:
            return RedirectResponse(url=state)
        return auth_info
