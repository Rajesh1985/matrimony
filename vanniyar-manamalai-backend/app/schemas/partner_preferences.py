from pydantic import BaseModel, Field, validator
from typing import Optional, List

class PartnerPreferencesBase(BaseModel):
    """Base schema with common fields"""
    profile_id: int
    age_from: Optional[int] = Field(default=None, ge=18, le=100, description="Minimum age preference")
    age_to: Optional[int] = Field(default=None, ge=18, le=100, description="Maximum age preference")
    height_from: Optional[int] = Field(default=None, ge=100, le=250, description="Minimum height in cm")
    height_to: Optional[int] = Field(default=None, ge=100, le=250, description="Maximum height in cm")
    education_preference: Optional[str] = Field(default=None, description="Comma-separated education levels")
    occupation_preference: Optional[str] = Field(default=None, description="Comma-separated occupations")
    income_preference: Optional[str] = Field(default=None, description="Income range preference")
    star_preference: Optional[str] = Field(default=None, description="Comma-separated star/nakshatra names")
    rasi_preference: Optional[str] = Field(default=None, description="Comma-separated rasi/zodiac signs")
    location_preference: Optional[str] = Field(default=None, description="Comma-separated locations")

    @validator('age_to')
    def validate_age_range(cls, v, values):
        """Ensure age_to >= age_from"""
        if v is not None and 'age_from' in values and values['age_from'] is not None:
            if v < values['age_from']:
                raise ValueError('age_to must be greater than or equal to age_from')
        return v

    @validator('height_to')
    def validate_height_range(cls, v, values):
        """Ensure height_to >= height_from"""
        if v is not None and 'height_from' in values and values['height_from'] is not None:
            if v < values['height_from']:
                raise ValueError('height_to must be greater than or equal to height_from')
        return v

class PartnerPreferencesCreate(PartnerPreferencesBase):
    """Schema for creating partner preferences"""
    pass

class PartnerPreferencesUpdate(BaseModel):
    """Schema for updating partner preferences - all fields optional"""
    age_from: Optional[int] = Field(default=None, ge=18, le=100)
    age_to: Optional[int] = Field(default=None, ge=18, le=100)
    height_from: Optional[int] = Field(default=None, ge=100, le=250)
    height_to: Optional[int] = Field(default=None, ge=100, le=250)
    education_preference: Optional[str] = None
    occupation_preference: Optional[str] = None
    income_preference: Optional[str] = None
    star_preference: Optional[str] = None
    rasi_preference: Optional[str] = None
    location_preference: Optional[str] = None

class PartnerPreferencesResponse(PartnerPreferencesBase):
    """Schema for partner preferences responses"""
    id: int

    class Config:
        orm_mode = True
        from_attributes = True

# Helper schemas for structured preferences
class PreferenceOptions(BaseModel):
    """Common preference options for UI dropdowns"""
    education_options: List[str] = [
        "High School", "Bachelor's Degree", "Master's Degree", 
        "PhD", "Diploma", "Professional Degree"
    ]
    occupation_options: List[str] = [
        "Engineer", "Doctor", "Teacher", "Business", "Government Job",
        "IT Professional", "Lawyer", "Accountant", "Entrepreneur", "Other"
    ]
    income_options: List[str] = [
        "Below 3 LPA", "3-5 LPA", "5-10 LPA", "10-15 LPA", 
        "15-20 LPA", "20-30 LPA", "30+ LPA"
    ]
    location_options: List[str] = [
        "Chennai", "Bangalore", "Hyderabad", "Mumbai", "Delhi",
        "USA", "UK", "Canada", "Australia", "Singapore", "UAE"
    ]

class MatchScore(BaseModel):
    """Match score between profile and partner preferences"""
    profile_id: int
    match_percentage: float
    age_match: bool
    height_match: bool
    education_match: bool
    occupation_match: bool
    star_match: bool
    rasi_match: bool
    location_match: bool
    matched_criteria: List[str]
    unmatched_criteria: List[str]
