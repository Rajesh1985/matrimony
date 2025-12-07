from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class GenderEnum(str, Enum):
    """Gender options"""
    Male = "Male"
    Female = "Female"
    Other = "Other"

class UserBase(BaseModel):
    """Base user schema"""
    country_code: str = Field(..., min_length=1, max_length=5, description="Country calling code (e.g., +91)")
    name: str = Field(..., min_length=1, max_length=100, description="Full name")
    mobile: str = Field(..., min_length=10, max_length=15, description="Mobile number without country code")
    email_id: EmailStr = Field(..., description="Email address")
    gender: GenderEnum

    @validator('mobile')
    def validate_mobile(cls, v):
        """Validate mobile number format"""
        if not v.isdigit():
            raise ValueError('Mobile number must contain only digits')
        if len(v) < 10:
            raise ValueError('Mobile number must be at least 10 digits')
        return v

class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(..., min_length=6, description="Password (minimum 6 characters)")

class UserUpdate(BaseModel):
    """Schema for updating user - excludes profile_id (immutable)"""
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    email_id: Optional[EmailStr] = None
    gender: Optional[GenderEnum] = None
    # Note: profile_id is NOT included - it's immutable after assignment

class UserUpdateMobile(BaseModel):
    """Schema for updating mobile number by profile_id"""
    new_mobile: str = Field(..., min_length=10, max_length=15, description="New mobile number")
    otp_code: Optional[str] = Field(default=None, max_length=6, description="OTP for verification")

    @validator('new_mobile')
    def validate_mobile(cls, v):
        """Validate mobile number format"""
        if not v.isdigit():
            raise ValueError('Mobile number must contain only digits')
        if len(v) < 10:
            raise ValueError('Mobile number must be at least 10 digits')
        return v

class UserResponse(UserBase):
    """Schema for user responses"""
    id: int
    profile_id: Optional[int]
    is_verified: bool

    class Config:
        orm_mode = True
        from_attributes = True

class UserLogin(BaseModel):
    """Schema for login"""
    mobile: str
    password: str

class UserValidationRequest(BaseModel):
    """Schema for user validation (deprecated - use UserLogin)"""
    mobile: str
    password: str

class OTPRequest(BaseModel):
    """Schema for OTP operations"""
    mobile: str

class OTPVerify(BaseModel):
    """Schema for OTP verification"""
    mobile: str
    otp_code: str = Field(..., min_length=4, max_length=6)

class PasswordUpdate(BaseModel):
    """Schema for password update"""
    old_password: str
    new_password: str = Field(..., min_length=6)

class UserSearchFilters(BaseModel):
    """Schema for user search filters"""
    gender: Optional[GenderEnum] = None
    is_verified: Optional[bool] = None
    has_profile: Optional[bool] = None  # Whether profile_id is set
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=100, ge=1, le=100)
