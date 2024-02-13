from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .repository import RefRepository


def get_ref_repository(get_async_session):
    def _get_ref_repository(session: AsyncSession = Depends(get_async_session)) -> RefRepository:
        return RefRepository(session)

    return _get_ref_repository
