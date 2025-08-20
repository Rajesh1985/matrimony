from pydantic import BaseModel

class UserBase(BaseModel):
    country_code: str
    mobile: str
    name: str = None  # Use default None for optional string
    email_id: str = None
    gender: str = None

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    profile_id: int

    class Config:
        orm_mode = True
