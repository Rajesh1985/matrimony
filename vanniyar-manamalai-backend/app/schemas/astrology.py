from pydantic import BaseModel, Field, validator
from typing import Optional
from enum import Enum

class StarEnum(str, Enum):
    """27 Nakshatras with Tamil mappings"""
    Ashwini = "Ashwini"
    Bharani = "Bharani"
    Krittika = "Krittika"
    Rohini = "Rohini"
    Arudra = "Arudra"
    Punarvasu = "Punarvasu"
    Pushya = "Pushya"
    Ashlesha = "Ashlesha"
    Magha = "Magha"
    Purva_Phalguni = "Purva Phalguni"
    Uttara_Phalguni = "Uttara Phalguni"
    Hasta = "Hasta"
    Chitra = "Chitra"
    Swati = "Swati"
    Vishakha = "Vishakha"
    Anuradha = "Anuradha"
    Jyeshtha = "Jyeshtha"
    Mula = "Mula"
    Purva_Ashadha = "Purva Ashadha"
    Uttara_Ashadha = "Uttara Ashadha"
    Shravana = "Shravana"
    Dhanishta = "Dhanishta"
    Shatabhisha = "Shatabhisha"
    Purva_Bhadrapada = "Purva Bhadrapada"
    Uttara_Bhadrapada = "Uttara Bhadrapada"
    Revati = "Revati"

class RasiEnum(str, Enum):
    """12 Zodiac Signs with Tamil mappings"""
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

class KotturaEnum(str, Enum):
    """Gothram/Kotturam"""
    Jumbo_Maha_Rishi = "Jumbo Maha Rishi"

class AstrologyDetailsBase(BaseModel):
    """Base schema with common fields"""
    profile_id: int
    star: Optional[StarEnum] = None
    rasi: Optional[RasiEnum] = None
    lagnam: Optional[str] = None
    birth_place: Optional[str] = None
    Kotturam: Optional[KotturaEnum] = None
    dosham_details: Optional[str] = None
    file_id: Optional[str] = Field(None, description="UUID reference to horoscope file")

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
