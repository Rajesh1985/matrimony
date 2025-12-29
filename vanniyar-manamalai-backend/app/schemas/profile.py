from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date, time, datetime

# ============================================================================
# VALIDATION CONSTANTS
# ============================================================================
# These constants define valid values for VARCHAR fields
# Keep in sync with frontend registration-data.constants.ts

VALID_GENDERS = {"Male", "Female", "Other"}
VALID_PHYSICAL_STATUS = {"Normal", "Physically Challenged"}
VALID_MARITAL_STATUS = {"Unmarried", "Widow_Widower", "Divorced", "Separated"}
VALID_FOOD_PREFERENCES = {"Veg", "NonVeg"}

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
    gender: str  # VARCHAR: Male, Female, Other
    hobbies: Optional[str] = None
    about_me: Optional[str] = None
    physical_status: Optional[str] = None  # VARCHAR: Normal, Physically Challenged
    marital_status: Optional[str] = None  # VARCHAR: Unmarried, Widow_Widower, Divorced, Separated
    food_preference: Optional[str] = None  # VARCHAR: Veg, NonVeg
    religion: Optional[str] = "hindu"
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    is_active: Optional[bool] = True

    @validator('gender')
    @classmethod
    def validate_gender(cls, v):
        if v and v not in VALID_GENDERS:
            raise ValueError(f'Gender must be one of {VALID_GENDERS}')
        return v

    @validator('physical_status')
    @classmethod
    def validate_physical_status(cls, v):
        if v and v not in VALID_PHYSICAL_STATUS:
            raise ValueError(f'Physical status must be one of {VALID_PHYSICAL_STATUS}')
        return v

    @validator('marital_status')
    @classmethod
    def validate_marital_status(cls, v):
        if v and v not in VALID_MARITAL_STATUS:
            raise ValueError(f'Marital status must be one of {VALID_MARITAL_STATUS}')
        return v

    @validator('food_preference')
    @classmethod
    def validate_food_preference(cls, v):
        if v and v not in VALID_FOOD_PREFERENCES:
            raise ValueError(f'Food preference must be one of {VALID_FOOD_PREFERENCES}')
        return v

class ProfileCreate(ProfileBase):
    """Schema for creating a new profile"""
    pass

class ProfileUpdate(BaseModel):
    """Schema for updating profile - all fields optional"""
    name: Optional[str] = None
    birth_date: Optional[str] = None  # Accept string, convert or leave None
    birth_time: Optional[str] = None  # Accept string, convert or leave None
    height_cm: Optional[int] = None
    complexion: Optional[str] = None
    caste: Optional[str] = None
    mobile_number: Optional[str] = None
    mobile: Optional[str] = None  # Alternative field name for mobile_number (for API compatibility)
    introducer_name: Optional[str] = None
    introducer_mobile: Optional[str] = None
    gender: Optional[str] = None  # VARCHAR: Male, Female, Other
    hobbies: Optional[str] = None
    about_me: Optional[str] = None
    physical_status: Optional[str] = None  # VARCHAR: Normal, Physically Challenged
    marital_status: Optional[str] = None  # VARCHAR: Unmarried, Widow_Widower, Divorced, Separated
    food_preference: Optional[str] = None  # VARCHAR: Veg, NonVeg
    religion: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    is_active: Optional[bool] = None

    @validator('birth_date', pre=True, always=False)
    @classmethod
    def validate_birth_date(cls, v):
        # Allow empty strings and None
        if v == '' or v is None:
            return None
        # If it's a string, try to parse it as a date
        if isinstance(v, str):
            try:
                return date.fromisoformat(v)
            except (ValueError, TypeError):
                return v  # Return as-is, let SQLAlchemy handle conversion
        return v

    @validator('birth_time', pre=True, always=False)
    @classmethod
    def validate_birth_time(cls, v):
        # Allow empty strings and None
        if v == '' or v is None:
            return None
        # If it's a string, try to parse it as a time
        if isinstance(v, str):
            try:
                return time.fromisoformat(v)
            except (ValueError, TypeError):
                return v  # Return as-is, let SQLAlchemy handle conversion
        return v

    @validator('gender', pre=True)
    @classmethod
    def validate_gender(cls, v):
        if v and v not in VALID_GENDERS:
            raise ValueError(f'Gender must be one of {VALID_GENDERS}')
        return v

    @validator('physical_status', pre=True)
    @classmethod
    def validate_physical_status(cls, v):
        if v and v not in VALID_PHYSICAL_STATUS:
            raise ValueError(f'Physical status must be one of {VALID_PHYSICAL_STATUS}')
        return v

    @validator('marital_status', pre=True)
    @classmethod
    def validate_marital_status(cls, v):
        if v and v not in VALID_MARITAL_STATUS:
            raise ValueError(f'Marital status must be one of {VALID_MARITAL_STATUS}')
        return v

    @validator('food_preference', pre=True)
    @classmethod
    def validate_food_preference(cls, v):
        if v and v not in VALID_FOOD_PREFERENCES:
            raise ValueError(f'Food preference must be one of {VALID_FOOD_PREFERENCES}')
        return v

class ProfileResponse(BaseModel):
    """Schema for profile responses"""
    id: int
    serial_number: Optional[str] = None
    name: str
    birth_date: Optional[date] = None
    birth_time: Optional[time] = None
    height_cm: Optional[int] = None
    complexion: Optional[str] = None
    caste: Optional[str] = None
    mobile_number: Optional[str] = None
    introducer_name: Optional[str] = None
    introducer_mobile: Optional[str] = None
    gender: str
    hobbies: Optional[str] = None
    about_me: Optional[str] = None
    physical_status: Optional[str] = None
    marital_status: Optional[str] = None
    food_preference: Optional[str] = None
    religion: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    is_active: Optional[bool] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True
