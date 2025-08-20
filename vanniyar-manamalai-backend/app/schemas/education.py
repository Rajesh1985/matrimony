from pydantic import BaseModel
from typing import Optional

class EducationDetailsSchema(BaseModel):
    profile_id: int
    degree: Optional[str]
    specialization: Optional[str]
    institution: Optional[str]
    location: Optional[str]
    year_of_completion: Optional[int]
    grade_percentage: Optional[float]

    class Config:
        orm_mode = True
