from sqlalchemy import Column, Integer, String, Date, ForeignKey, DECIMAL, Text
from database import Base

class PropertyDetails(Base):
    __tablename__ = "property_details"
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"))
    property_type = Column(String(20))
    property_value = Column(DECIMAL(15,2))
    location = Column(String(200))
    description = Column(Text)
