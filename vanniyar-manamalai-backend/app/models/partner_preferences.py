from sqlalchemy import Column, Integer, ForeignKey, Text
from app.database import Base

class PartnerPreferences(Base):
    __tablename__ = "partner_preferences"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    
    # Age range preferences
    age_from = Column(Integer)
    age_to = Column(Integer)
    
    # Height range preferences (in cm)
    height_from = Column(Integer)
    height_to = Column(Integer)
    
    # Qualification and career preferences
    education_preference = Column(Text)  # e.g., "Bachelor's, Master's, PhD"
    occupation_preference = Column(Text)  # e.g., "Engineer, Doctor, Business"
    income_preference = Column(Text)  # e.g., "5-10 LPA, 10-20 LPA, 20+ LPA"
    
    # Astrological preferences (comma-separated)
    star_preference = Column(Text)  # e.g., "Rohini, Ashwini, Bharani"
    rasi_preference = Column(Text)  # e.g., "Aries, Taurus, Leo"
    
    # Location preferences
    location_preference = Column(Text)  # e.g., "Chennai, Bangalore, USA, UK"
