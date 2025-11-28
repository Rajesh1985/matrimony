from pydantic import BaseModel, Field, validator
from typing import Optional
from enum import Enum

class StarEnum(str, Enum):
    """27 Nakshatras with Tamil mappings"""
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

class RasiEnum(str, Enum):
    """12 Zodiac Signs with Tamil mappings"""
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

class KotturaEnum(str, Enum):
    """Gothram/Kotturam"""
    jumbo_maha_rishi = "Jumbo Maha Rishi Kotturam"

class AstrologyDetailsBase(BaseModel):
    """Base schema with common fields"""
    profile_id: int
    star: Optional[StarEnum] = None
    rasi: Optional[RasiEnum] = None
    lagnam: Optional[str] = None
    birth_place: Optional[str] = None
    Kotturam: Optional[KotturaEnum] = None
    dosham_details: Optional[str] = None
    file_id: str = Field(..., description="UUID reference to horoscope file")

class AstrologyDetailsCreate(AstrologyDetailsBase):
    """Schema for creating astrology details"""
    pass

class AstrologyDetailsUpdate(BaseModel):
    """Schema for updating astrology details - all fields optional"""
    star: Optional[StarEnum] = None
    rasi: Optional[RasiEnum] = None
    lagnam: Optional[str] = None
    birth_place: Optional[str] = None
    Kotturam: Optional[KotturaEnum] = None
    dosham_details: Optional[str] = None
    file_id: Optional[str] = None

class AstrologyDetailsResponse(AstrologyDetailsBase):
    """Schema for astrology responses"""
    id: int

    class Config:
        orm_mode = True
        from_attributes = True

# Tamil UI mapping reference for frontend
STAR_TAMIL_MAP = {
    "Ashwini": "அசுவனி",
    "Bharani": "பரணி",
    "Krittika": "கார்த்திகை",
    "Rohini": "ரோகிணி",
    "Arudra": "திருவாதிரை",
    "Punarvasu": "புனர்பூசம்",
    "Pushya": "பூசம்",
    "Ashlesha": "ஆயில்யம்",
    "Magha": "மகம்",
    "Purva Phalguni": "பூரம்",
    "Uttara Phalguni": "உத்திரம்",
    "Hasta": "அஸ்தம்",
    "Chitra": "சித்திரை",
    "Swati": "சுவாதி",
    "Vishakha": "விசாகம்",
    "Anuradha": "அனுஷம்",
    "Jyeshtha": "கேட்டை",
    "Mula": "மூலம்",
    "Purva Ashadha": "பூராடம்",
    "Uttara Ashadha": "உத்திராடம்",
    "Shravana": "திருவோணம்",
    "Dhanishta": "அவிட்டம்",
    "Shatabhisha": "சதயம்",
    "Purva Bhadrapada": "பூரட்டாதி",
    "Uttara Bhadrapada": "உத்திரட்டாதி",
    "Revati": "ரேவதி"
}

RASI_TAMIL_MAP = {
    "Aries": "மேஷம்",
    "Taurus": "ரிஷபம்",
    "Gemini": "மிதுனம்",
    "Cancer": "கடகம்",
    "Leo": "சிம்மம்",
    "Virgo": "கன்னி",
    "Libra": "துலாம்",
    "Scorpio": "விருச்சிகம்",
    "Sagittarius": "தனுசு",
    "Capricorn": "மகரம்",
    "Aquarius": "கும்பம்",
    "Pisces": "மீனம்"
}
