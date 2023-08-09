"""Photom exceptions"""

from fastapi import HTTPException, status


class NotAuthorized(HTTPException):
    """Not authorized - 401"""

    def __init__(self, detail: str = "Not authorized"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
