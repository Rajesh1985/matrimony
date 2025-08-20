from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base

class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    address_type = Column(String(20))
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    is_primary = Column(Boolean, default=False)
