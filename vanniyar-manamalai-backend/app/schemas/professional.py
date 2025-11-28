from pydantic import BaseModel, Field, validator
from typing import Optional
from enum import Enum

class EmploymentTypeEnum(str, Enum):
    """Employment status categories"""
    employed = "Employed"
    self_employed = "Self-employed"
    business = "Business"
    unemployed = "Unemployed"
    student = "Student"
    retired = "Retired"

class ProfessionalDetailsBase(BaseModel):
    """Base schema with common fields"""
    profile_id: int
    education: Optional[str] = Field(default=None, description="Primary education qualification")
    education_optional: Optional[str] = Field(default=None, description="Additional qualifications (MBA, PhD, etc.)")
    employment_type: Optional[str] = Field(default=None, description="Employment status")
    occupation: Optional[str] = Field(default=None, description="Occupation/profession")
    company_name: Optional[str] = Field(default=None, description="Company/organization name")
    annual_income: Optional[str] = Field(default=None, description="Annual income range (e.g., '5-10 LPA')")
    work_location: Optional[str] = Field(default=None, description="Work city/country")

class ProfessionalDetailsCreate(ProfessionalDetailsBase):
    """Schema for creating professional details"""
    pass

class ProfessionalDetailsUpdate(BaseModel):
    """Schema for updating professional details - all fields optional"""
    education: Optional[str] = None
    education_optional: Optional[str] = None
    employment_type: Optional[str] = None
    occupation: Optional[str] = None
    company_name: Optional[str] = None
    annual_income: Optional[str] = None
    work_location: Optional[str] = None

class ProfessionalDetailsResponse(ProfessionalDetailsBase):
    """Schema for professional responses"""
    id: int

    class Config:
        orm_mode = True
        from_attributes = True

# Helper schemas for UI options
class ProfessionalOptions(BaseModel):
    """Standard options for professional dropdowns"""
    education_options: list[str] = [
        "High School", "Diploma", "Bachelor's Degree", "Master's Degree",
        "PhD", "Engineering", "Medical", "Law", "Commerce", "Arts",
        "Science", "Computer Science", "MBA", "CA", "CS"
    ]
    employment_type_options: list[str] = [
        "Employed", "Self-employed", "Business", "Unemployed", "Student", "Retired"
    ]
    occupation_options: list[str] = [
        "Engineer", "Doctor", "Teacher", "Software Developer", "Manager",
        "Business Owner", "Lawyer", "Accountant", "Government Employee",
        "Bank Employee", "Consultant", "Entrepreneur", "Freelancer",
        "Architect", "Pharmacist", "Nurse", "Professor", "Scientist"
    ]
    income_options: list[str] = [
        "Below 3 LPA", "3-5 LPA", "5-10 LPA", "10-15 LPA", "15-20 LPA",
        "20-30 LPA", "30-50 LPA", "50 LPA+", "1 Cr+"
    ]
    location_options: list[str] = [
        "Chennai", "Bangalore", "Hyderabad", "Mumbai", "Delhi", "Pune",
        "Coimbatore", "Madurai", "USA", "UK", "Canada", "Australia",
        "Singapore", "UAE", "Germany", "Other"
    ]

class ProfessionalSummary(BaseModel):
    """Professional info summary for display"""
    education_summary: str  # e.g., "B.E. + MBA"
    employment_summary: str  # e.g., "Employed at TCS, Chennai"
    income_summary: str  # e.g., "10-15 LPA"
    is_employed: bool
    has_advanced_degree: bool

    @staticmethod
    def from_professional_details(prof: ProfessionalDetailsResponse) -> 'ProfessionalSummary':
        """Generate summary from professional details"""
        # Education summary
        edu_parts = [prof.education] if prof.education else []
        if prof.education_optional:
            edu_parts.append(prof.education_optional)
        education_summary = " + ".join(edu_parts) if edu_parts else "Not specified"
        
        # Employment summary
        employment_parts = []
        if prof.employment_type:
            employment_parts.append(prof.employment_type)
        if prof.occupation:
            employment_parts.append(f"as {prof.occupation}")
        if prof.company_name:
            employment_parts.append(f"at {prof.company_name}")
        if prof.work_location:
            employment_parts.append(f"in {prof.work_location}")
        employment_summary = " ".join(employment_parts) if employment_parts else "Not specified"
        
        # Income summary
        income_summary = prof.annual_income if prof.annual_income else "Not specified"
        
        # Flags
        is_employed = prof.employment_type in ["Employed", "Self-employed", "Business"] if prof.employment_type else False
        has_advanced_degree = any(keyword in (prof.education_optional or "").lower() 
                                  for keyword in ["mba", "phd", "master", "m.tech", "m.e.", "ca", "cs"])
        
        return ProfessionalSummary(
            education_summary=education_summary,
            employment_summary=employment_summary,
            income_summary=income_summary,
            is_employed=is_employed,
            has_advanced_degree=has_advanced_degree
        )
