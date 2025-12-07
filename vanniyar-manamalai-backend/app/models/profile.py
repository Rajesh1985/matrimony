from sqlalchemy import Column, Integer, String, Date, Time, Boolean, DateTime, Enum
from datetime import datetime
from app.database import Base
import enum

class GenderEnum(str, enum.Enum):
    Male = "Male"
    Female = "Female"
    Other = "Other"

class PhysicalStatusEnum(str, enum.Enum):
    Normal = "Normal"
    Physically_Challenged = "Physically Challenged"

class MaritalStatusEnum(str, enum.Enum):
    Unmarried = "Unmarried"
    Widow_Widower = "Widow_Widower"
    Divorced = "Divorced"
    Separated = "Separated"

class FoodPreferenceEnum(str, enum.Enum):
    Veg = "Veg"
    NonVeg = "NonVeg"

class Profile(Base):
    __tablename__ = "profiles"
    __table_args__ = {'implicit_returning': False}

    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String(20), unique=True)
    name = Column(String(100), nullable=False)
    birth_date = Column(Date)
    birth_time = Column(Time)
    height_cm = Column(Integer)
    complexion = Column(String(50))
    caste = Column(String(100), default='Vanniyar')
    mobile_number = Column(String(20))
    introducer_name = Column(String(100))
    introducer_mobile = Column(String(20))
    gender = Column(Enum(GenderEnum, native_enum=True), nullable=False)
    hobbies = Column(String(500))
    about_me = Column(String(2048))
    physical_status = Column(Enum(PhysicalStatusEnum, native_enum=True))
    marital_status = Column(Enum(MaritalStatusEnum, native_enum=True))
    food_preference = Column(Enum(FoodPreferenceEnum, native_enum=True))
    religion = Column(String(50), default='hindu')
    address_line1 = Column(String(255))
    address_line2 = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    postal_code = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
