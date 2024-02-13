from typing import Optional

from fastapi import APIRouter, Depends

from db import get_async_session
from . import schemas
from .dependencies import get_auth_repository
from .repository import AuthRepository

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register/", response_model=schemas.UserRead)
async def create_user(
        user: schemas.UserCreate,
        referral_code: Optional[str] = None,
        repository: AuthRepository = Depends(get_auth_repository(get_async_session))
):
    user = await repository.create_user(user, referral_code)

    return user
