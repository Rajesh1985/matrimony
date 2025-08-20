from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text
from database import Base

class FamilyDetails(Base):
    __tablename__ = "family_details"
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"))
    father_name = Column(String(100))
    father_occupation = Column(String(100))
    mother_name = Column(String(100))
    mother_occupation = Column(String(100))
    total_siblings = Column(Integer, default=0)
    married_siblings = Column(Integer, default=0)
    family_type = Column(String(20), default='nuclear')
    family_status = Column(String(100))
    family_values = Column(Text)
