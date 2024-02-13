from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .repository import AuthRepository


def get_auth_repository(get_async_session):
    def _get_auth_repository(session: AsyncSession = Depends(get_async_session)) -> AuthRepository:
        return AuthRepository(session)

    return _get_auth_repository
