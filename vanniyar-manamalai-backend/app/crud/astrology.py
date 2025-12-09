from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..models.astrology import AstrologyDetails
from ..schemas.astrology import AstrologyDetailsCreate, AstrologyDetailsUpdate
from fastapi import HTTPException

def create_astrology(db: Session, astrology_data: AstrologyDetailsCreate):
    """
    Create new astrology details for a profile
    
    Purpose: Store horoscope data when user uploads during registration/profile completion
    """
    try:
        db_astrology = AstrologyDetails(**astrology_data.dict())
        db.add(db_astrology)
        db.commit()
        db.refresh(db_astrology)
        return db_astrology
    except IntegrityError as e:
        db.rollback()
        if "foreign key constraint" in str(e).lower():
            raise HTTPException(status_code=400, detail="Invalid profile_id: Profile does not exist")
        raise HTTPException(status_code=400, detail="Database integrity error")

def get_astrology_by_id(db: Session, astrology_id: int):
    """
    Get astrology details by ID
    
    Purpose: Retrieve specific astrology record (admin operations)
    """
    return db.query(AstrologyDetails).filter(AstrologyDetails.id == astrology_id).first()

def get_astrology_by_profile(db: Session, profile_id: int):
    """
    Get all astrology details for a specific profile
    
    Purpose: Display horoscope info on profile page
    Note: Returns list (though typically 1 record per profile)
    """
    return db.query(AstrologyDetails).filter(AstrologyDetails.profile_id == profile_id).all()

def update_astrology(db: Session, astrology_id: int, astrology_data: AstrologyDetailsUpdate):
    """
    Update astrology details (partial update)
    
    Purpose: Allow users to modify horoscope info or upload new horoscope file
    Use Cases:
    - User corrects star/rasi after consulting astrologer
    - User uploads better quality horoscope file
    - Admin updates dosham details after review
    """
    db_astrology = db.query(AstrologyDetails).filter(AstrologyDetails.id == astrology_id).first()
    
    if not db_astrology:
        return None
    
    # Update only provided fields
    update_data = astrology_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_astrology, field, value)
    
    db.commit()
    db.refresh(db_astrology)
    return db_astrology

def delete_astrology(db: Session, astrology_id: int):
    """
    Delete astrology details
    
    Purpose: Remove horoscope data (user privacy request or data cleanup)
    Note: CASCADE delete will happen automatically if profile is deleted
    """
    db_astrology = db.query(AstrologyDetails).filter(AstrologyDetails.id == astrology_id).first()
    
    if not db_astrology:
        return None
    
    db.delete(db_astrology)
    db.commit()
    return db_astrology

def get_profiles_by_star(db: Session, star: str, skip: int = 0, limit: int = 100):
    """
    Find profiles by star/nakshatra
    
    Purpose: Matching algorithm - find compatible partners by star
    Use Case: "Find all Rohini star profiles"
    """
    return (
        db.query(AstrologyDetails)
        .filter(AstrologyDetails.star == star)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_profiles_by_rasi(db: Session, rasi: str, skip: int = 0, limit: int = 100):
    """
    Find profiles by rasi/zodiac sign
    
    Purpose: Matching algorithm - find compatible partners by rasi
    Use Case: "Find all Leo/சிம்மம் profiles"
    """
    return (
        db.query(AstrologyDetails)
        .filter(AstrologyDetails.rasi == rasi)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_profiles_by_star_and_rasi(db: Session, star: str, rasi: str, skip: int = 0, limit: int = 100):
    """
    Find profiles by both star and rasi
    
    Purpose: Advanced matching - more precise astrological compatibility
    Use Case: "Find profiles with Rohini star AND Taurus rasi"
    """
    return (
        db.query(AstrologyDetails)
        .filter(AstrologyDetails.star == star, AstrologyDetails.rasi == rasi)
        .offset(skip)
        .limit(limit)
        .all()
    )

def update_astrology_by_profile_id(db: Session, profile_id: int, astrology_data: AstrologyDetailsUpdate):
    """
    Update astrology details by profile_id (partial update)
    
    Purpose: Update horoscope directly from profile context
    
    Why This is Needed:
    - Simpler API for frontend: no need to fetch astrology_id first
    - Direct profile-based workflow: "Update horoscope for profile #123"
    - Reduces API calls: 2 calls (get astrology_id → update) becomes 1 call
    
    Use Cases:
    1. Profile edit page: User updates horoscope without knowing astrology_id
    2. Admin editing profile: Update horoscope data directly
    3. Mobile app: Simpler state management (store profile_id only)
    
    Example Workflow:
    Frontend has profile_id from login/session
    → Directly call PATCH /astrology/profile/123
    → No need to GET /astrology/profile/123 first to find astrology_id
    
    Returns: Updated astrology record or None if not found
    """
    # Find astrology record by profile_id
    db_astrology = db.query(AstrologyDetails).filter(
        AstrologyDetails.profile_id == profile_id
    ).first()
    
    if not db_astrology:
        return None
    
    # Update only provided fields
    update_data = astrology_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_astrology, field, value)
    
    db.commit()
    db.refresh(db_astrology)
    return db_astrology


def delete_astrology_by_profile_id(db: Session, profile_id: int):
    """
    Delete astrology details by profile_id
    
    Purpose: Remove horoscope data using profile reference
    
    Why This is Needed:
    - Profile-centric deletion: "Remove horoscope for profile #123"
    - Simpler frontend logic: no need to fetch astrology_id first
    - Batch operations: When deactivating profile, remove related data
    
    Use Cases:
    1. User requests horoscope removal (privacy)
    2. Profile deactivation workflow: Remove all profile data including horoscope
    3. Admin cleanup: Remove horoscope for specific profile
    4. User uploaded wrong horoscope: Delete and re-upload
    
    Example Workflow:
    User in profile settings → "Remove Horoscope" button
    → DELETE /astrology/profile/123
    → No need to know astrology_id
    
    Note: 
    - If multiple astrology records exist for profile (shouldn't happen, but handles edge case)
    - Returns count of deleted records
    """
    # Find all astrology records for this profile
    db_astrology_records = db.query(AstrologyDetails).filter(
        AstrologyDetails.profile_id == profile_id
    ).all()
    
    if not db_astrology_records:
        return None
    
    # Delete all astrology records for this profile
    deleted_count = 0
    for record in db_astrology_records:
        db.delete(record)
        deleted_count += 1
    
    db.commit()
    
    return deleted_count
