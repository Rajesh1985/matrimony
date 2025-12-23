from pydantic import BaseModel
from typing import Optional
from datetime import date, time, datetime
from enum import Enum

class GenderEnum(str, Enum):
    Male = "Male"
    Female = "Female"
    Other = "Other"

class PhysicalStatusEnum(str, Enum):
    Normal = "Normal"
    Physically_Challenged = "Physically_Challenged"

class MaritalStatusEnum(str, Enum):
    Unmarried = "Unmarried"
    Widow_Widower = "Widow_Widower"
    Divorced = "Divorced"
    Separated = "Separated"

class FoodPreferenceEnum(str, Enum):
    Veg = "Veg"
    Non_Veg = "NonVeg"

class CompleteProfileResponse(BaseModel):
    """
    Complete Profile Response Schema
    Combines data from multiple tables: Users, Profiles, Astrology, Professional, Family, Partner Preferences
    """
    
    # User Info
    user_id: int
    email_id: Optional[str] = None
    mobile: Optional[str] = None
    country_code: Optional[str] = None
    is_verified: Optional[bool] = False
    
    # Profile Info
    profile_id: int
    name: str
    serial_number: Optional[str] = None
    birth_date: Optional[date] = None
    birth_time: Optional[time] = None
    height_cm: Optional[int] = None
    complexion: Optional[str] = None
    caste: Optional[str] = None
    gender: GenderEnum
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
    profile_created_at: Optional[datetime] = None
    profile_updated_at: Optional[datetime] = None
    age: Optional[int] = None
    
    # Astrology Info
    star: Optional[str] = None
    rasi: Optional[str] = None
    lagnam: Optional[str] = None
    birth_place: Optional[str] = None
    dosham_details: Optional[str] = None
    astrology_file_id: Optional[str] = None
    
    # Professional Info
    education: Optional[str] = None
    education_optional: Optional[str] = None
    employment_type: Optional[str] = None
    occupation: Optional[str] = None
    company_name: Optional[str] = None
    annual_income: Optional[str] = None
    work_location: Optional[str] = None
    
    # Family Info
    father_name: Optional[str] = None
    father_occupation: Optional[str] = None
    mother_name: Optional[str] = None
    mother_occupation: Optional[str] = None
    family_type: Optional[str] = None
    family_status: Optional[str] = None
    brothers: Optional[int] = None
    sisters: Optional[int] = None
    married_brothers: Optional[int] = None
    married_sisters: Optional[int] = None
    family_description: Optional[str] = None
    community_file_id: Optional[str] = None
    photo_file_id_1: Optional[str] = None
    photo_file_id_2: Optional[str] = None
    
    # Partner Preferences Info
    age_from: Optional[int] = None
    age_to: Optional[int] = None
    height_from: Optional[int] = None
    height_to: Optional[int] = None
    education_preference: Optional[str] = None
    occupation_preference: Optional[str] = None
    income_preference: Optional[str] = None
    location_preference: Optional[str] = None
    star_preference: Optional[str] = None
    rasi_preference: Optional[str] = None

    class Config:
        use_enum_values = True
        orm_mode = True
        from_attributes = True
