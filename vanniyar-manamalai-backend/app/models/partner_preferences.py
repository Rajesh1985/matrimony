from sqlalchemy import Column, Integer, String, ForeignKey, Text
from database import Base

class PartnerPreferences(Base):
    __tablename__ = "partner_preferences"
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"))
    age_from = Column(Integer)
    age_to = Column(Integer)
    height_from = Column(Integer)
    height_to = Column(Integer)
    education_preference = Column(Text)
    occupation_preference = Column(Text)
    income_preference = Column(Text)
    caste_preference = Column(Text)
    star_preference = Column(Text)
    rasi_preference = Column(Text)
    location_preference = Column(Text)
    other_preferences = Column(Text)
