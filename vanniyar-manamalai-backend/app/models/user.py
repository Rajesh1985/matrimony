from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from app.database import Base
import enum

class GenderEnum(str, enum.Enum):
    """Gender options"""
    Male = "Male"
    Female = "Female"
    Other = "Other"

class User(Base):
    __tablename__ = "Users"  # Note: Capital 'U' to match SQL schema
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    country_code = Column(String(5), nullable=False)
    name = Column(String(100), nullable=False)
    mobile = Column(String(15), unique=True)  # UNIQUE constraint for mobile
    email_id = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)  # Should be hashed in production
    profile_id = Column(Integer, nullable=True)  # Nullable - assigned after profile creation
    is_verified = Column(Boolean, default=False)
    otp_code = Column(String(6), nullable=True)
    otp_created_at = Column(DateTime, nullable=True)
    gender = Column(Enum(GenderEnum), nullable=False)
