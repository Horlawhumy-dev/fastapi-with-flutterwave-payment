

from typing import Annotated
from fastapi import Depends, HTTPException, Header
import jwt

from .config import env_vars


JWT_KEY_ID = env_vars.JWT_KEY_ID
JWT_SIGNATURE_ALGORITHM = env_vars.JWT_SIGNATURE_ALGORITHM


async def get_token(token: Annotated[str, Header(description="JWT of a signed in user")]):
    return token


async def get_current_user(token: Annotated[str, Depends(get_token)]):
    # TODO: Secure this process>>>>use Python-jose packkage
    try:
        payload = jwt.decode(token, algorithms=[JWT_SIGNATURE_ALGORITHM], options={
                             "verify_signature": False})
        sub: str = payload.get('sub')
    except:
        raise HTTPException(
            status_code=401,
            detail="Unable to validate token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    else:
        return sub
