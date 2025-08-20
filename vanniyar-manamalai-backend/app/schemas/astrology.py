from pydantic import BaseModel
from typing import Optional

class AstrologyDetailsSchema(BaseModel):
    profile_id: int
    star: Optional[str]
    rasi: Optional[str]
    lagnam: Optional[str]
    birth_place: Optional[str]
    gotram: Optional[str]
    dosham_details: Optional[str]
    horoscope_url: Optional[str]

    class Config:
        orm_mode = True
