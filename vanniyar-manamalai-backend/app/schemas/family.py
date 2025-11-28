from pydantic import BaseModel, Field, validator
from typing import Optional
from enum import Enum

class FamilyStatusEnum(str, Enum):
    """Economic status of family"""
    middle_class = "Middle_Class"
    upper_middle_class = "upper_middle_class"
    rich_elite = "Rich/Elite"

class FamilyTypeEnum(str, Enum):
    """Family structure type"""
    nuclear = "nuclear"
    joint = "joint"
    extended = "extended"

class FamilyDetailsBase(BaseModel):
    """Base schema with common fields"""
    profile_id: int
    father_name: Optional[str] = None
    father_occupation: Optional[str] = None
    mother_name: Optional[str] = None
    mother_occupation: Optional[str] = None
    brothers: Optional[int] = Field(default=0, ge=0, description="Number of brothers")
    sisters: Optional[int] = Field(default=0, ge=0, description="Number of sisters")
    Married_brothers: Optional[int] = Field(default=0, ge=0, description="Number of married brothers")
    Married_sisters: Optional[int] = Field(default=0, ge=0, description="Number of married sisters")
    family_type: Optional[FamilyTypeEnum] = FamilyTypeEnum.nuclear
    family_status: Optional[FamilyStatusEnum] = None
    Family_description: Optional[str] = None

    @validator('Married_brothers')
    def validate_married_brothers(cls, v, values):
        """Ensure married brothers <= total brothers"""
        if 'brothers' in values and v > values['brothers']:
            raise ValueError('Married brothers cannot exceed total brothers')
        return v

    @validator('Married_sisters')
    def validate_married_sisters(cls, v, values):
        """Ensure married sisters <= total sisters"""
        if 'sisters' in values and v > values['sisters']:
            raise ValueError('Married sisters cannot exceed total sisters')
        return v

class FamilyDetailsCreate(FamilyDetailsBase):
    """Schema for creating family details"""
    pass

class FamilyDetailsUpdate(BaseModel):
    """Schema for updating family details - all fields optional"""
    father_name: Optional[str] = None
    father_occupation: Optional[str] = None
    mother_name: Optional[str] = None
    mother_occupation: Optional[str] = None
    brothers: Optional[int] = Field(default=None, ge=0)
    sisters: Optional[int] = Field(default=None, ge=0)
    Married_brothers: Optional[int] = Field(default=None, ge=0)
    Married_sisters: Optional[int] = Field(default=None, ge=0)
    family_type: Optional[FamilyTypeEnum] = None
    family_status: Optional[FamilyStatusEnum] = None
    Family_description: Optional[str] = None

class FamilyDetailsResponse(FamilyDetailsBase):
    """Schema for family responses"""
    id: int

    class Config:
        orm_mode = True
        from_attributes = True

# Helper class for computed properties
class FamilySummary(BaseModel):
    """Computed family statistics"""
    total_siblings: int
    total_married_siblings: int
    unmarried_brothers: int
    unmarried_sisters: int
    total_unmarried_siblings: int

    @staticmethod
    def from_family_details(family: FamilyDetailsResponse) -> 'FamilySummary':
        """Calculate summary from family details"""
        total_siblings = (family.brothers or 0) + (family.sisters or 0)
        total_married = (family.Married_brothers or 0) + (family.Married_sisters or 0)
        unmarried_brothers = (family.brothers or 0) - (family.Married_brothers or 0)
        unmarried_sisters = (family.sisters or 0) - (family.Married_sisters or 0)
        
        return FamilySummary(
            total_siblings=total_siblings,
            total_married_siblings=total_married,
            unmarried_brothers=unmarried_brothers,
            unmarried_sisters=unmarried_sisters,
            total_unmarried_siblings=unmarried_brothers + unmarried_sisters
        )
