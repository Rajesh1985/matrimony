from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    country_code = Column(String(5), nullable=False)
    name = Column(String(100), nullable=True)
    mobile = Column(String(15), unique=True, nullable=False)
    email_id = Column(String(255), nullable=True)
    password = Column(String(255), nullable=False)
    profile_id = Column(Integer, nullable=False)
    is_verified = Column(Boolean, default=False)
    otp_code = Column(String(6), nullable=True)
    otp_created_at = Column(DateTime, nullable=True)
    gender = Column(String(10), nullable=True)