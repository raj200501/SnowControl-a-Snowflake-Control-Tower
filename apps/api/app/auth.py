from __future__ import annotations

from fastapi import Depends, Header, HTTPException, status

from app.settings import get_settings


def require_local_token(authorization: str | None = Header(default=None)) -> str:
    settings = get_settings()
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or token != settings.local_dev_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")
    return token


def require_auth(token: str = Depends(require_local_token)) -> str:
    return token
