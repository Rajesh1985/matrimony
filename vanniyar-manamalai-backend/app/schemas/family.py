from pydantic import BaseModel
from typing import Optional

class FamilyDetailsSchema(BaseModel):
    profile_id: int
    father_name: Optional[str]
    father_occupation: Optional[str]
    mother_name: Optional[str]
    mother_occupation: Optional[str]
    total_siblings: Optional[int]
    married_siblings: Optional[int]
    family_type: Optional[str]
    family_status: Optional[str]
    family_values: Optional[str]

    class Config:
        orm_mode = True
