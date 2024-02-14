from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from fastapi_users.password import PasswordHelper
from sqlalchemy import select, exc
from sqlalchemy.ext.asyncio import AsyncSession

from utils.logger import logger

from . import models, schemas
from .schemas import UserRead


class AuthRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_referrer_by_code(self, referral_code: str) -> UserRead:
        try:
            stmt = select(models.User).where(models.User.referral_code == referral_code)
            result = await self.session.execute(stmt)
            return result.scalars().first()
        except Exception as e:
            logger.error(e)
            raise

    async def email_exists(self, email: str) -> bool:
        try:
            stmt = select(models.User).where(models.User.email == email)
            existing_user = await self.session.execute(stmt)
            return bool(existing_user.one_or_none())
        except Exception as e:
            logger.error(e)
            raise

    async def create_user(self, user: schemas.UserCreate, referral_code: Optional[str]) -> dict:
        referrer_id = None

        if referral_code:
            referrer = await self.get_referrer_by_code(referral_code)
            referrer_id = referrer.id

        user = user.dict()
        password = user.pop("password")
        db_user = models.User(**user)
        db_user.referrer_id = referrer_id
        password_helper = PasswordHelper()
        db_user.hashed_password = password_helper.hash(password)

        try:
            self.session.add(db_user)
            await self.session.commit()
        except exc.SQLAlchemyError as e:
            logger.error(e)
            raise

        return db_user.json()
