from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, CHAR
from app.database import Base
import enum

class StarEnum(str, enum.Enum):
    """27 Nakshatras (Tamil: நட்சத்திரங்கள்)"""
    ashwini = "Ashwini"
    bharani = "Bharani"
    krittika = "Krittika"
    rohini = "Rohini"
    arudra = "Arudra"
    punarvasu = "Punarvasu"
    pushya = "Pushya"
    ashlesha = "Ashlesha"
    magha = "Magha"
    purva_phalguni = "Purva Phalguni"
    uttara_phalguni = "Uttara Phalguni"
    hasta = "Hasta"
    chitra = "Chitra"
    swati = "Swati"
    vishakha = "Vishakha"
    anuradha = "Anuradha"
    jyeshtha = "Jyeshtha"
    mula = "Mula"
    purva_ashadha = "Purva Ashadha"
    uttara_ashadha = "Uttara Ashadha"
    shravana = "Shravana"
    dhanishta = "Dhanishta"
    shatabhisha = "Shatabhisha"
    purva_bhadrapada = "Purva Bhadrapada"
    uttara_bhadrapada = "Uttara Bhadrapada"
    revati = "Revati"

class RasiEnum(str, enum.Enum):
    """12 Zodiac Signs (Tamil: ராசி)"""
    aries = "Aries"
    taurus = "Taurus"
    gemini = "Gemini"
    cancer = "Cancer"
    leo = "Leo"
    virgo = "Virgo"
    libra = "Libra"
    scorpio = "Scorpio"
    sagittarius = "Sagittarius"
    capricorn = "Capricorn"
    aquarius = "Aquarius"
    pisces = "Pisces"

class KotturaEnum(str, enum.Enum):
    """Gothram (Tamil: கோத்திரம்)"""
    jumbo_maha_rishi = "Jumbo Maha Rishi Kotturam"

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
    file_id = Column(CHAR(36), nullable=False)  # UUID for horoscope file reference
