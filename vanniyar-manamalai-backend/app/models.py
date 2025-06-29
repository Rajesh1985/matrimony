from sqlalchemy import Column, Integer, String, Date, Time, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Profile(Base):
    __tablename__ = "profiles"
    __table_args__ = {'implicit_returning': False}
    
    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String(20), unique=True)
    name = Column(String(100))
    birth_date = Column(Date)
    birth_time = Column(Time)
    height_cm = Column(Integer)
    complexion = Column(String(50))
    caste = Column(String(100))
    sub_caste = Column(String(100))
    mobile_number = Column(String(20))
    is_active = Column(Boolean, default=True)

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    address_type = Column(String(20))
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    is_primary = Column(Boolean, default=False)