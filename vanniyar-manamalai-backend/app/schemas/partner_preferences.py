from pydantic import BaseModel
from typing import Optional

class PartnerPreferencesSchema(BaseModel):
    profile_id: int
    age_from: Optional[int]
    age_to: Optional[int]
    height_from: Optional[int]
    height_to: Optional[int]
    education_preference: Optional[str]
    occupation_preference: Optional[str]
    income_preference: Optional[str]
    caste_preference: Optional[str]
    star_preference: Optional[str]
    rasi_preference: Optional[str]
    location_preference: Optional[str]
    other_preferences: Optional[str]

    class Config:
        orm_mode = True
