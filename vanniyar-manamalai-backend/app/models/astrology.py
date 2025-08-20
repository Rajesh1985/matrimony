from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class AstrologyDetails(Base):
    __tablename__ = "astrology_details"
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"))
    star = Column(String(50))
    rasi = Column(String(50))
    lagnam = Column(String(50))
    birth_place = Column(String(100))
    gotram = Column(String(50))
    dosham_details = Column(String)
    horoscope_url = Column(String(255))
