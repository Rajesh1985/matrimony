from pydantic import BaseModel
from typing import Optional
from enum import Enum


class GenderEnum(str, Enum):
    Male = "Male"
    Female = "Female"
    Other = "Other"


class RecommendedProfileResponse(BaseModel):
    """
    Recommended Profile Response Schema
    
    Returns profile recommendations based on partner preferences matching
    Data from vw_profile_recommendations view with match scoring
    
    Attributes:
        current_profile_id: Profile ID of the user requesting recommendations
        current_user_id: User ID of the person requesting
        match_profile_id: Profile ID of the recommended match
        match_user_id: User ID of the recommended match
        name: Full name of the recommended profile
        age: Calculated age of the recommended profile
        height_cm: Height in centimeters
        gender: Gender of the recommended profile
        occupation: Job occupation/title
        star: Astrological star (Nakshatra)
        rasi: Astrological sign (Zodiac)
        city: City name
        state: State/Province
        country: Country name
        about_me: Personal description/bio
        match_score: Compatibility score (0-8 scale)
            - 0: No matches
            - 8: Perfect match on all criteria
    
    Example:
        {
            "current_profile_id": 4,
            "current_user_id": 3,
            "match_profile_id": 6,
            "match_user_id": 5,
            "name": "Rajeshkumar",
            "age": 40,
            "height_cm": 170,
            "gender": "Male",
            "occupation": "IAS",
            "star": "Ashwini",
            "rasi": "Taurus",
            "city": "Madurai",
            "state": "Tamil Nadu",
            "country": "India",
            "about_me": "I am Rajesh. Working as Engineer",
            "match_score": 0
        }
    """
    
    # Current Profile (User requesting recommendations)
    current_profile_id: int
    current_user_id: int
    
    # Recommended Match Profile
    match_profile_id: int
    match_user_id: int
    serial_number: Optional[str] = None
    
    # Match Profile Details
    name: str
    age: int
    height_cm: Optional[int] = None
    gender: GenderEnum
    occupation: Optional[str] = None
    
    # Astrological Info
    star: Optional[str] = None
    rasi: Optional[str] = None
    
    # Location Info
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    
    # Profile Info
    about_me: Optional[str] = None
    
    # Photo File IDs for displaying profile photos
    photo_file_id_1: Optional[str] = None
    photo_file_id_2: Optional[str] = None
    
    # Matching Score
    match_score: int  # 0-8 scale based on preference matching

    class Config:
        from_attributes = True
