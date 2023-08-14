"""ASGI Application for photom."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from photom.config import EnvProxy
from photom.version import __version__

from ._auth import auth

app = FastAPI(title="Photom API", version=__version__)

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=True
)

app.include_router(auth)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=EnvProxy.get_str("HOST") or "127.0.0.1", port=EnvProxy.get_int("PORT") or 3000)
