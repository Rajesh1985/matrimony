from pydantic import BaseModel
from typing import Optional, List
from datetime import date, time

class AddressSchema(BaseModel):
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    is_primary: bool = False

    class Config:
        orm_mode = True

class ProfileSchema(BaseModel):
    name: str
    birth_date: Optional[date]
    birth_time: Optional[time]
    height_cm: Optional[int]
    complexion: Optional[str]
    caste: Optional[str]
    sub_caste: Optional[str]
    mobile_number: Optional[str]
    is_active: bool = True

    class Config:
        orm_mode = True

class AstrologySchema(BaseModel):
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
