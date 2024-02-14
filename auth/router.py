from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from config import settings
from db import get_async_session
from utils.apiclient import HunterEmailVerifierClient
from utils.logger import logger
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
    logger.info(f"Attempting to register user {user.email}")

    if referral_code:
        referrer = await repository.get_referrer_by_code(referral_code)
        if referrer is None:
            logger.warning(f"Invalid referral code {referral_code} provided")
            raise HTTPException(status_code=400, detail="Invalid referral code")
        if referrer.referral_code_expiration < datetime.now():
            logger.warning(f"Referral code {referral_code} has expired")
            raise HTTPException(status_code=400, detail="Referral code is expired")

    email_exists = await repository.email_exists(user.email)
    if email_exists:
        logger.warning(f"User with email {user.email} already exists")
        raise HTTPException(status_code=400, detail="User with this email already exists")

    email_allowed = await hunter_client.email_allowed(user.email)
    if not email_allowed:
        logger.warning(f"Registration at email address {user.email} is not allowed")
        raise HTTPException(status_code=400, detail="Registration at this email address is not available")

    user = await repository.create_user(user, referral_code)
    logger.info(f"User {user.get('email')}({user.get('id')}) has registered")

    return user
