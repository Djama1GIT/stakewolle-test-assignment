from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship

from db import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, index=True, unique=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    referral_code = Column(Text, nullable=True, unique=True)
    referral_expiration = Column(DateTime, nullable=True)
    referrer_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    referrals = relationship("User", backref="referrals_backref", remote_side=[id])

