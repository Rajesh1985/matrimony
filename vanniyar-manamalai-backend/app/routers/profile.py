from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileResponse
from app.crud.profile import create_profile, get_profile, get_profiles, update_profile, delete_profile
from app.models.profile import Profile

router = APIRouter(prefix="/profiles", tags=["profiles"])

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
