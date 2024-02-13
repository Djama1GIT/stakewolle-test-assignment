import datetime
from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    referral_code: Optional[str] = None
    referral_expiration: Optional[datetime.datetime] = None
    referrer_id: Optional[int] = None
    referrals: Optional[list['UserRead']] = None
    referrer: Optional['UserRead'] = None


class UserCreate(schemas.BaseUserCreate):
    # referral_code: Optional[str] = None
    # referral_expiration: Optional[datetime.datetime] = None
    # referrer_id: Optional[int] = None
    pass


class UserUpdate(schemas.BaseUserUpdate):
    referral_code: Optional[str] = None
    referral_expiration: Optional[datetime.datetime] = None
    referrer_id: Optional[int] = None
