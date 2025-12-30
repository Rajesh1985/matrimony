from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, CHAR
from app.database import Base
import enum

class StarEnum(str, enum.Enum):
    """27 Nakshatras (Tamil: நட்சத்திரங்கள்)"""
    Ashwini = "Ashwini"
    Bharani = "Bharani"
    Krittika = "Krittika"
    Rohini = "Rohini"
    Mrigashirsha = "Mrigashirsha"
    Arudra = "Arudra"
    Punarvasu = "Punarvasu"
    Pushya = "Pushya"
    Ashlesha = "Ashlesha"
    Magha = "Magha"
    Purva_Phalguni = "Purva_Phalguni"
    Uttara_Phalguni = "Uttara_Phalguni"
    Hasta = "Hasta"
    Chitra = "Chitra"
    Swati = "Swati"
    Vishakha = "Vishakha"
    Anuradha = "Anuradha"
    Jyeshtha = "Jyeshtha"
    Mula = "Mula"
    Purva_Ashadha = "Purva_Ashadha"
    Uttara_Ashadha = "Uttara_Ashadha"
    Shravana = "Shravana"
    Dhanishta = "Dhanishta"
    Shatabhisha = "Shatabhisha"
    Purva_Bhadrapada = "Purva_Bhadrapada"
    Uttara_Bhadrapada = "Uttara_Bhadrapada"
    Revati = "Revati"

class RasiEnum(str, enum.Enum):
    """12 Zodiac Signs (Tamil: ராசி)"""
    Aries = "Aries"
    Taurus = "Taurus"
    Gemini = "Gemini"
    Cancer = "Cancer"
    Leo = "Leo"
    Virgo = "Virgo"
    Libra = "Libra"
    Scorpio = "Scorpio"
    Sagittarius = "Sagittarius"
    Capricorn = "Capricorn"
    Aquarius = "Aquarius"
    Pisces = "Pisces"

class KotturaEnum(str, enum.Enum):
    """Gothram (Tamil: கோத்திரம்)"""
    Jumbo_Maha_Rishi = "Jumbo Maha Rishi"

class AstrologyDetails(Base):
    __tablename__ = "astrology_details"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    star = Column(Enum(StarEnum))
    rasi = Column(Enum(RasiEnum))
    lagnam = Column(String(100))
    birth_place = Column(String(100))
    Kotturam = Column(Enum(KotturaEnum))
    dosham_details = Column(Text)
    file_id = Column(CHAR(36), nullable=True)  # UUID for horoscope file reference (optional)
