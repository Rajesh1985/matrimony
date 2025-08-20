from pydantic import BaseModel
from typing import Optional

class ProfessionalDetailsSchema(BaseModel):
    profile_id: int
    designation: Optional[str]
    company_name: Optional[str]
    industry: Optional[str]
    experience_years: Optional[float]
    monthly_income: Optional[float]
    annual_income: Optional[float]
    work_location: Optional[str]

    class Config:
        orm_mode = True
