from pydantic import BaseModel
from typing import Optional

class AddressSchema(BaseModel):
    profile_id: int
    address_type: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    is_primary: Optional[bool] = False

    class Config:
        orm_mode = True
