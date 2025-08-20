from sqlalchemy import Column, Integer, String, Date, Time, Boolean
from database import Base

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
