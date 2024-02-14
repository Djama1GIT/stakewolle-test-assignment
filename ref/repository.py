from datetime import datetime, timedelta
from typing import Sequence

from fastapi_cache.decorator import cache

from sqlalchemy import select, update, exists
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from utils.logger import logger


class RefRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_referrals_by_id(self, id_: int) -> Sequence | None:
        try:
            exist_stmt = select(exists().where(User.id == id_))
            result = await self.session.execute(exist_stmt)
            does_exist = result.scalar()

            if not does_exist:
                logger.error(f"Referrer ID {id_} does not exist.")
                return None

            stmt = select(User.id).where(User.referrer_id == id_)
            result = await self.session.execute(stmt)
            referrals = result.scalars().all()
            return referrals
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Error when receiving referrals by ID: {e}")
            raise

    @cache(expire=3600)
    async def get_code_by_email(self, email: str) -> str | None:
        try:
            stmt = select(User.referral_code).where(User.email == email)
            result = await self.session.execute(stmt)
            user_code = result.scalar_one()
            return user_code
        except NoResultFound:
            return None
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Error when receiving user code by email: {e}")
            raise

    async def get_id_by_email(self, email: str) -> int | None:
        try:
            stmt = select(User.id).where(User.email == email)
            result = await self.session.execute(stmt)
            user_id = result.scalar_one()
            return user_id
        except NoResultFound:
            return None
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Error when receiving user ID by email: {e}")
            raise

    # async def get_referrals_by_email(self, email: str) -> Sequence | None:
    #     try:
    #         user_id = await self.get_id_by_email(email)
    #         if user_id is not None:
    #             stmt = select(User.id).where(User.referrer_id == user_id)
    #             result = await self.session.execute(stmt)
    #             referrals = result.scalars().all()
    #             return referrals
    #         else:
    #             return None
    #     except SQLAlchemyError as e:
    #         await self.session.rollback()
    #         logger.error(f"Error when receiving referrals by email: {e}")
    #         raise

    async def get_id_by_code(self, code: str) -> int | None:
        try:
            stmt = select(User.id).where(User.referral_code == code)
            result = await self.session.execute(stmt)
            user_id = result.scalar_one()
            return user_id
        except NoResultFound:
            return None
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Error when getting the user ID by code: {e}")
            raise

    # async def get_referrals_by_code(self, code: str) -> Sequence | None:
    #     try:
    #         user_id = await self.get_id_by_code(code)
    #         if user_id is not None:
    #             stmt = select(User.id).where(User.referrer_id == user_id)
    #             result = await self.session.execute(stmt)
    #             referrals = result.scalars().all()
    #             return referrals
    #         else:
    #             return None
    #     except SQLAlchemyError as e:
    #         await self.session.rollback()
    #         logger.error(f"Error when receiving referrals by code: {e}")
    #         raise

    async def create_code_for_user_by_id(self, id_: int, code: str, expiration: int) -> None:
        try:
            stmt = update(User).where(User.id == id_).values(
                referral_code=code,
                referral_code_expiration=datetime.now() + timedelta(days=expiration),
            )
            await self.session.execute(stmt)
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Error when creating code for the user: {e}")
            raise

    async def delete_code_for_user_by_id(self, id_: int) -> None:
        try:
            stmt = update(User).where(User.id == id_).values(referral_code=None, referral_code_expiration=None)
            await self.session.execute(stmt)
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Error deleting the code for the user: {e}")
            raise
