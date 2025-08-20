from pydantic import BaseModel
from typing import Optional

class ProfilePhotoSchema(BaseModel):
    profile_id: int
    photo_url: Optional[str]
    photo_type: Optional[str]
    upload_date: Optional[str]
    is_primary: Optional[bool] = False

    class Config:
        orm_mode = True
