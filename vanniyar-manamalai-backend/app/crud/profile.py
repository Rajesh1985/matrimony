from sqlalchemy.orm import Session
from ..models.profile import Profile
from ..schemas.profile import ProfileCreate, ProfileUpdate

def create_profile(db: Session, profile_data: ProfileCreate):
    """Create a new profile"""
    db_profile = Profile(**profile_data.dict())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def get_profile(db: Session, profile_id: int):
    """Get profile by ID"""
    return db.query(Profile).filter(Profile.id == profile_id).first()

def get_profiles(db: Session, skip: int = 0, limit: int = 100):
    """Get all profiles with pagination"""
    return db.query(Profile).offset(skip).limit(limit).all()

def update_serial_number_by_profile_id(db: Session, profile_id: int, serial_number: str):
    """Update verification status"""
    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    
    if not db_profile:
        return None
    
    db_profile.serial_number = serial_number
    
    db.commit()
    db.refresh(db_profile)
    return db_profile

def update_profile(db: Session, profile_id: int, profile_data: ProfileUpdate):
    """
    Update profile with partial data (only fields provided)
    
    Purpose: Allows users to update specific profile fields without sending entire object
    Example: Update only mobile_number without needing to send name, birth_date, etc.
    """
    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    
    if not db_profile:
        return None
    
    # Update only fields that are provided (not None)
    update_data = profile_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_profile, field, value)
    
    db.commit()
    db.refresh(db_profile)
    return db_profile

def delete_profile(db: Session, profile_id: int):
    """Soft delete profile by setting is_active to False"""
    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    
    if not db_profile:
        return None
    
    db_profile.is_active = False
    db.commit()
    return db_profile
