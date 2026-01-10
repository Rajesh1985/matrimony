from pydantic import BaseModel
from typing import Optional

class ProfileSummaryResponse(BaseModel):
    user_id: int
    profile_id: int
    serial_number: Optional[str]
    name: str
    email_id: str
    mobile: str
    gender: str
    city: str
    state: str

    class Config:
        orm_mode = True
        from_attributes = True
