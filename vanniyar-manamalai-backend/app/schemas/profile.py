from pydantic import BaseModel
from typing import Optional
from datetime import date, time

class ProfileSchema(BaseModel):
    name: str
    birth_date: date
    birth_time: Optional[time]
    height_cm: Optional[int]
    complexion: Optional[str]
    caste: Optional[str]
    sub_caste: Optional[str]
    mobile_number: Optional[str]
    is_active: Optional[bool] = True

    class Config:
        orm_mode = True
