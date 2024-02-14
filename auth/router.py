from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from config import settings
from db import get_async_session
from utils.apiclient import HunterEmailVerifierClient
from . import schemas
from .dependencies import get_auth_repository
from .repository import AuthRepository

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

hunter_client = HunterEmailVerifierClient(settings.HUNTER_EMAIL_VERIFIER_API_KEY)


@router.post("/register/", response_model=schemas.UserRead)
async def create_user(
        user: schemas.UserCreate,
        referral_code: Optional[str] = None,
        repository: AuthRepository = Depends(get_auth_repository(get_async_session))
):
    if referral_code:
        referrer = await repository.get_referrer_by_code(referral_code)
        if referrer is None:
            raise HTTPException(status_code=400, detail="Invalid referral code")
        if referrer.referral_code_expiration < datetime.now():
            raise HTTPException(status_code=400, detail="Referral code is expired")

    if repository.email_exists(user.email):
        raise HTTPException(status_code=400, detail="User with this email already exists")

    if not hunter_client.email_allowed(user.email):
        raise HTTPException(status_code=400, detail="Registration at this email address is not available")

    user = await repository.create_user(user, referral_code)

    return user
