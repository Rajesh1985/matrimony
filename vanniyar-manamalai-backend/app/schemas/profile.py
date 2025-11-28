from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time, datetime
from enum import Enum

class GenderEnum(str, Enum):
    male = "Male"
    female = "Female"
    other = "Other"

class PhysicalStatusEnum(str, Enum):
    normal = "Normal"
    physically_challenged = "Physically Challenged"

class MaritalStatusEnum(str, Enum):
    unmarried = "Unmarried"
    widow_widower = "Widow_Widower"
    divorced = "Divorced"
    separated = "Separated"

class FoodPreferenceEnum(str, Enum):
    veg = "Veg"
    non_veg = "NonVeg"

class ProfileBase(BaseModel):
    name: str
    birth_date: date
    birth_time: Optional[time] = None
    height_cm: Optional[int] = None
    complexion: Optional[str] = None
    caste: Optional[str] = "Vanniyar"
    mobile_number: Optional[str] = None
    introducer_name: Optional[str] = None
    introducer_mobile: Optional[str] = None
    gender: GenderEnum
    hobbies: Optional[str] = None
    about_me: Optional[str] = None
    physical_status: Optional[PhysicalStatusEnum] = None
    marital_status: Optional[MaritalStatusEnum] = None
    food_preference: Optional[FoodPreferenceEnum] = None
    religion: Optional[str] = "hindu"
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    is_active: Optional[bool] = True

class ProfileCreate(ProfileBase):
    """Schema for creating a new profile"""
    pass

class ProfileUpdate(BaseModel):
    """Schema for updating profile - all fields optional"""
    name: Optional[str] = None
    birth_date: Optional[date] = None
    birth_time: Optional[time] = None
    height_cm: Optional[int] = None
    complexion: Optional[str] = None
    caste: Optional[str] = None
    mobile_number: Optional[str] = None
    introducer_name: Optional[str] = None
    introducer_mobile: Optional[str] = None
    gender: Optional[GenderEnum] = None
    hobbies: Optional[str] = None
    about_me: Optional[str] = None
    physical_status: Optional[PhysicalStatusEnum] = None
    marital_status: Optional[MaritalStatusEnum] = None
    food_preference: Optional[FoodPreferenceEnum] = None
    religion: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    is_active: Optional[bool] = None

class ProfileResponse(ProfileBase):
    """Schema for profile responses"""
    id: int
    serial_number: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True
