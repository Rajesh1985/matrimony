from pydantic import BaseModel
from typing import Optional

class PropertyDetailsSchema(BaseModel):
    profile_id: int
    property_type: Optional[str]
    property_value: Optional[float]
    location: Optional[str]
    description: Optional[str]

    class Config:
        orm_mode = True
