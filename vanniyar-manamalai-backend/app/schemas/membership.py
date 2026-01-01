from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date
from enum import Enum


class PlanNameEnum(str, Enum):
    """Valid membership plan names"""
    Silver = "Silver"
    Gold = "Gold"
    Platinum = "Platinum"


class MembershipBase(BaseModel):
    """Base membership schema"""
    plan_name: Optional[str] = Field(None, description="Membership plan name: Silver, Gold, or Platinum")

    @validator('plan_name')
    def validate_plan_name(cls, v):
        """Validate plan_name is one of the valid options or None"""
        if v is not None and v not in {"Silver", "Gold", "Platinum"}:
            raise ValueError('Invalid plan name. Must be Silver, Gold, or Platinum')
        return v


class MembershipCreateRequest(BaseModel):
    """Schema for creating new membership"""
    profile_id: int = Field(..., gt=0, description="Profile ID (must be positive)")
    plan_name: str = Field(..., description="Membership plan name: Silver, Gold, or Platinum")

    @validator('plan_name')
    def validate_plan_name(cls, v):
        """Validate plan_name is one of the valid options"""
        if v not in {"Silver", "Gold", "Platinum"}:
            raise ValueError('Invalid plan name. Must be Silver, Gold, or Platinum')
        return v


class MembershipUpdateRequest(BaseModel):
    """Schema for updating membership"""
    plan_name: Optional[str] = Field(None, description="Membership plan name: Silver, Gold, Platinum, or null to cancel")

    @validator('plan_name')
    def validate_plan_name(cls, v):
        """Validate plan_name is one of the valid options or None"""
        if v is not None and v not in {"Silver", "Gold", "Platinum"}:
            raise ValueError('Invalid plan name. Must be Silver, Gold, or Platinum')
        return v


class MembershipResponse(BaseModel):
    """Schema for membership response"""
    membership_id: int = Field(..., description="Unique membership record ID")
    profile_id: int = Field(..., description="Profile ID associated with this membership")
    plan_name: Optional[str] = Field(None, description="Membership plan name: Silver, Gold, Platinum, or null")
    start_date: Optional[date] = Field(None, description="Membership start date")
    end_date: Optional[date] = Field(None, description="Membership end/expiry date")

    class Config:
        from_attributes = True
