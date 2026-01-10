from sqlalchemy import Column, Integer, String, Date, Time, Boolean, DateTime
from datetime import datetime
from app.database import Base

# ============================================================================
# VALIDATION CONSTANTS
# ============================================================================
# These constants define valid values for VARCHAR fields
# Keep in sync with frontend registration-data.constants.ts

VALID_GENDERS = {"Male", "Female", "Other"}
VALID_PHYSICAL_STATUS = {"Normal", "Physically Challenged"}
VALID_MARITAL_STATUS = {"Unmarried", "Widow_Widower", "Divorced", "Separated"}
VALID_FOOD_PREFERENCES = {"Veg", "NonVeg"}

class Profile(Base):
    """
    Profile Model - SQLAlchemy ORM model for profiles table
    All ENUM fields converted to VARCHAR with validation in Pydantic schemas
    """
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
    gender = Column(String(20), nullable=False)  # VARCHAR: Male, Female, Other
    hobbies = Column(String(500))
    about_me = Column(String(2048))
    physical_status = Column(String(50))  # VARCHAR: Normal, Physically Challenged
    marital_status = Column(String(50))  # VARCHAR: Unmarried, Widow_Widower, Divorced, Separated
    food_preference = Column(String(20))  # VARCHAR: Veg, NonVeg
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
