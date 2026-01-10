

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.database import get_db
from app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileResponse
from app.schemas.complete_profile import CompleteProfileResponse
from app.schemas.recommendation import RecommendedProfileResponse
from app.schemas.profile_summary import ProfileSummaryResponse
from app.crud.profile import create_profile, get_profile, get_profiles, update_profile, delete_profile, update_serial_number_by_profile_id
from app.crud.vw_user_profiles_complete import (
    get_profiles_complete,
    get_all_profiles_complete,
    get_recommended_profiles,
)
from app.models.profile import Profile
from app.models.user import User
from app.models.membership import MembershipDetails
from datetime import date
from pydantic import BaseModel

# === Admin credentials (static) ===
ADMIN_USERNAME = "manamalai_admin"
ADMIN_PASSWORD = "Chenagai@12345"

class AdminLoginRequest(BaseModel):
    username: str
    password: str

class AdminValidationResponse(BaseModel):
    valid: bool

class ProfileCountResponse(BaseModel):
    count: int

router = APIRouter(prefix="/profiles", tags=["profiles"])

# ===================== Custom Profile List Endpoints =====================

@router.post("/admin/validate", response_model=AdminValidationResponse)
def validate_admin(login: AdminLoginRequest):
    """
    Validate admin credentials (static, case-sensitive)
    """
    if login.username == ADMIN_USERNAME and login.password == ADMIN_PASSWORD:
        return {"valid": True}
    return {"valid": False}

# ===================== Count Endpoints =====================

@router.get("/Approved_list/count", response_model=ProfileCountResponse)
def get_approved_profiles_count(db: Session = Depends(get_db)):
    """
    Get count of approved profiles (is_verified == 1)
    """
    from sqlalchemy import text
    query = text("""
    SELECT COUNT(DISTINCT profile_id) as total
    FROM vw_user_profiles_complete
    WHERE is_verified = 1
    """)
    result = db.execute(query).fetchone()
    count = result[0] if result and result[0] else 0
    return {"count": count}


@router.get("/Unapproved_list/count", response_model=ProfileCountResponse)
def get_unapproved_profiles_count(db: Session = Depends(get_db)):
    """
    Get count of unapproved profiles (is_verified == 0)
    """
    from sqlalchemy import text
    query = text("""
    SELECT COUNT(DISTINCT profile_id) as total
    FROM vw_user_profiles_complete
    WHERE is_verified = 0
    """)
    result = db.execute(query).fetchone()
    count = result[0] if result and result[0] else 0
    return {"count": count}


@router.get("/exipred_list/count", response_model=ProfileCountResponse)
def get_expired_profiles_count(db: Session = Depends(get_db)):
    """
    Get count of expired profiles (membership expired or missing)
    """
    from sqlalchemy import text
    today = date.today()
    query = text("""
    SELECT COUNT(DISTINCT profile_id) as total
    FROM vw_user_profiles_complete
    WHERE is_verified = 1 AND (end_date < :today OR end_date IS NULL OR (plan_name IS NULL AND end_date IS NULL) OR (plan_name IS NOT NULL AND end_date IS NULL))
    """)
    result = db.execute(query, {"today": today}).fetchone()
    count = result[0] if result and result[0] else 0
    return {"count": count}


# ===================== Custom Profile List Endpoints =====================
@router.get("/Approved_list/all", response_model=None)
def get_approved_profiles(limit: int = Query(20, ge=1), offset: int = Query(0, ge=0), db: Session = Depends(get_db)):
    """
    Get all approved profiles (is_verified == 1)
    """
    from sqlalchemy import text
    query = text("""
    SELECT user_id, profile_id, serial_number, name, email_id, mobile, gender, city, state
    FROM vw_user_profiles_complete
    WHERE is_verified = 1
    ORDER BY profile_id ASC
    LIMIT :limit OFFSET :offset
    """)
    results = db.execute(query, {"limit": limit, "offset": offset}).fetchall()
    # Remove duplicates by (user_id, profile_id)
    unique = {}
    for row in results:
        key = (row[0], row[1])
        if key not in unique:
            unique[key] = {
                "user_id": int(row[0]),
                "profile_id": row[1],
                "serial_number": row[2],
                "name": row[3],
                "email_id": row[4],
                "mobile": row[5],
                "gender": row[6],
                "city": row[7],
                "state": row[8],
            }
    profiles = list(unique.values())
    if not profiles:
        return {"profiles": [], "message": "No approved profiles found"}
    return profiles


@router.get("/Unapproved_list/all", response_model=None)
def get_unapproved_profiles(limit: int = Query(20, ge=1), offset: int = Query(0, ge=0), db: Session = Depends(get_db)):
    """
    Get all unapproved profiles (is_verified == 0)
    """
    from sqlalchemy import text
    query = text("""
    SELECT user_id, profile_id, serial_number, name, email_id, mobile, gender, city, state
    FROM vw_user_profiles_complete
    WHERE is_verified = 0
    ORDER BY profile_id ASC
    LIMIT :limit OFFSET :offset
    """)
    results = db.execute(query, {"limit": limit, "offset": offset}).fetchall()
    unique = {}
    for row in results:
        key = (row[0], row[1])
        if key not in unique:
            unique[key] = {
                "user_id": row[0],
                "profile_id": row[1],
                "serial_number": row[2],
                "name": row[3],
                "email_id": row[4],
                "mobile": row[5],
                "gender": row[6],
                "city": row[7],
                "state": row[8],
            }
    profiles = list(unique.values())
    if not profiles:
        return {"profiles": [], "message": "No unapproved profiles found"}
    return profiles


@router.get("/exipred_list/all", response_model=None)
def get_expired_profiles(limit: int = Query(20, ge=1), offset: int = Query(0, ge=0), db: Session = Depends(get_db)):
    """
    Get all expired profiles (membership expired or missing)
    """
    today = date.today()
    from sqlalchemy import text
    query = text("""
    SELECT user_id, profile_id, serial_number, name, email_id, mobile, gender, city, state
    FROM vw_user_profiles_complete
    WHERE is_verified = 1 AND (end_date < :today OR end_date IS NULL OR (plan_name IS NULL AND end_date IS NULL) OR (plan_name IS NOT NULL AND end_date IS NULL))
    ORDER BY profile_id ASC
    LIMIT :limit OFFSET :offset
    """)
    results = db.execute(query, {"today": today, "limit": limit, "offset": offset}).fetchall()
    unique = {}
    for row in results:
        key = (row[0], row[1])
        if key not in unique:
            unique[key] = {
                "user_id": row[0],
                "profile_id": row[1],
                "serial_number": row[2],
                "name": row[3],
                "email_id": row[4],
                "mobile": row[5],
                "gender": row[6],
                "city": row[7],
                "state": row[8],
            }
    profiles = list(unique.values())
    if not profiles:
        return {"profiles": [], "message": "No expired profiles found"}
    return profiles

@router.get("/profile_id_by_mobile/{mobile}")
def get_profile_id_by_mobile_route(mobile: str, db: Session = Depends(get_db)):
    """
    Get profile ID by mobile number
    Purpose: Quick lookup for login/authentication flows
    """
    profile = db.query(Profile).filter(Profile.mobile_number == mobile).first()
    
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found for mobile")
    
    return {"profile_id": profile.id}

@router.post("/", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
def create_new_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
    """
    Create a new profile
    Purpose: Register new user in matrimony system
    """
    return create_profile(db, profile)

@router.get("/{profile_id}", response_model=ProfileResponse)
def read_profile(profile_id: int, db: Session = Depends(get_db)):
    """
    Get profile by ID
    Purpose: View complete profile details
    """
    db_profile = get_profile(db, profile_id)
    
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return db_profile

@router.get("/", response_model=list[ProfileResponse])
def read_profiles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all profiles with pagination
    Purpose: List profiles for browsing/matching
    """
    return get_profiles(db, skip=skip, limit=limit)

@router.put("/serial_number/{profile_id}")
def update_serial_number_by_profile(profile_id: int, serial_number: str, db: Session = Depends(get_db)):

    profile = update_serial_number_by_profile_id(db, profile_id, serial_number)
    
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return profile

@router.patch("/{profile_id}", response_model=ProfileResponse)
def update_profile_route(profile_id: int, profile: ProfileUpdate, db: Session = Depends(get_db)):
    """
    Update profile (partial update)
    
    Purpose: Allow users to update their profile information
    
    Why PATCH method:
    - PATCH = partial update (send only fields to change)
    - PUT = full replacement (must send all fields)
    
    Use Cases:
    1. User updates mobile number only
    2. User adds/updates address fields
    3. User modifies about_me text
    4. Admin updates marital_status
    
    Example Request:
    PATCH /profiles/123
    {
        "mobile_number": "9876543210",
        "city": "Chennai"
    }
    
    Only mobile_number and city will be updated, other fields remain unchanged.
    """
    print(f"[update_profile] Updating profile ID {profile_id} with data: {profile}")
    db_profile = update_profile(db, profile_id, profile)
    
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return db_profile

@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile_route(profile_id: int, db: Session = Depends(get_db)):
    """
    Soft delete profile
    Purpose: Deactivate profile instead of permanent deletion (data retention)
    """
    db_profile = delete_profile(db, profile_id)
    
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return None


# ============================================================================
# Complete Profile View Endpoints
# ============================================================================
# These endpoints query the vw_user_profiles_complete view which provides
# comprehensive profile data from multiple tables (Users, Profiles, Astrology, 
# Professional, Family, Partner Preferences)
# ============================================================================

@router.get("/complete/{profile_id}", response_model=CompleteProfileResponse)
def get_complete_profile(profile_id: int, db: Session = Depends(get_db)):
    """
    Get complete profile with all related information
    
    Purpose: Retrieve comprehensive profile data from vw_user_profiles_complete view
    
    Args:
        profile_id: The profile ID to retrieve
    
    Returns:
        CompleteProfileResponse with all profile details including:
        - User information
        - Profile details (basic info, address)
        - Astrology details
        - Professional details
        - Family details
        - Partner preferences
        - Calculated age
    
    Example:
        GET /profiles/complete/1
    """
    profile_data = get_profiles_complete(db, profile_id)
    
    if profile_data is None:
        raise HTTPException(status_code=404, detail="Complete profile not found")
    
    return profile_data


@router.get("/complete-list/all", response_model=list[CompleteProfileResponse])
def get_all_complete_profiles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all complete profiles with pagination
    
    Purpose: Retrieve all profiles with comprehensive details
    
    Args:
        skip: Number of records to skip (default: 0)
        limit: Maximum number of records to return (default: 100)
    
    Returns:
        List of CompleteProfileResponse objects
    
    Example:
        GET /profiles/complete-list/all?skip=0&limit=20
    """
    return get_all_profiles_complete(db, skip=skip, limit=limit)

@router.get("/recommendations/{profile_id}", response_model=list[RecommendedProfileResponse])
def get_recommended_profiles_route(profile_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get recommended profiles for a specific profile
    
    Purpose: Retrieve recommended profiles based on partner preferences matching
    Uses vw_profile_recommendations view with calculated match scores
    
    Args:
        profile_id: The profile ID to get recommendations for
        skip: Number of records to skip (default: 0)
        limit: Maximum number of records to return (default: 100)
    
    Returns:
        List of RecommendedProfileResponse objects ordered by match_score DESC
    
    Match Score Breakdown (0-8):
        - Age match: +1 if within preference range
        - Height match: +1 if within preference range
        - Education match: +1 if matches preference
        - Occupation match: +1 if matches preference
        - Income match: +1 if matches preference
        - Location match: +1 if matches preference
        - Star match: +1 if matches astrological preference
        - Rasi match: +1 if matches astrological preference
    
    Example:
        GET /profiles/recommendations/4?skip=0&limit=20
        
        Response:
        [
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
                "about_me": "I am Rajesh...",
                "match_score": 5
            }
        ]
    """
    recommendations = get_recommended_profiles(db, profile_id, skip=skip, limit=limit)
    
    if not recommendations:
        raise HTTPException(status_code=404, detail="No recommendations found for this profile")
    
    return recommendations