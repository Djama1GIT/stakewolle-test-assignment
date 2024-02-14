from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship

from db import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, index=True, unique=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    referral_code = Column(Text, nullable=True, unique=True, index=True)
    referral_code_expiration = Column(DateTime, nullable=True)
    referrer_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    referrals = relationship("User", backref="referrals_backref", remote_side=[id])

    def json(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
            "is_verified": self.is_verified,
            "referral_code": self.referral_code,
            "referral_code_expiration": str(self.referral_code_expiration),
            "referrer_id": self.referrer_id,
        }
