from typing import Optional

from fastapi import HTTPException
from fastapi_users.password import PasswordHelper
from sqlalchemy import select, exc
from sqlalchemy.ext.asyncio import AsyncSession

from logger import logger

from . import models, schemas


class AuthRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_referrer_by_code(self, referral_code: str):
        stmt = select(models.User).where(models.User.referral_code == referral_code)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def create_user(self, user: schemas.UserCreate, referral_code: Optional[str]):
        stmt = select(models.User).where(models.User.email == user.email)
        existing_user = await self.session.execute(stmt)
        if existing_user.one_or_none():
            raise HTTPException(status_code=400, detail="User with this email already exists")

        referrer = None

        if referral_code:
            referrer = await self.get_referrer_by_code(referral_code)
            if referrer is None:
                raise HTTPException(status_code=400, detail="Invalid referral code")
        logger.info("123", referrer.id, referrer)
        user = user.dict()
        password = user.pop("password")
        db_user = models.User(**user)
        db_user.referrer_id = referrer.id
        password_helper = PasswordHelper()
        db_user.hashed_password = password_helper.hash(password)

        try:
            self.session.add(db_user)
            await self.session.commit()
        except exc.SQLAlchemyError as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail="DB Error")

        return db_user.json()
