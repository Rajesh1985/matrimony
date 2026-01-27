from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..models.partner_preferences import PartnerPreferences
from ..schemas.partner_preferences import PartnerPreferencesCreate, PartnerPreferencesUpdate
from fastapi import HTTPException

def create_partner_preferences(db: Session, preferences_data: PartnerPreferencesCreate):
    """
    Create new partner preferences for a profile
    
    Purpose: Store partner requirements when user fills preference form
    """
    try:
        db_preferences = PartnerPreferences(**preferences_data.dict())
        db.add(db_preferences)
        db.commit()
        db.refresh(db_preferences)
        return db_preferences
    except IntegrityError as e:
        db.rollback()
        if "foreign key constraint" in str(e).lower():
            raise HTTPException(status_code=400, detail="Invalid profile_id: Profile does not exist")
        raise HTTPException(status_code=400, detail="Database integrity error")

def get_preferences_by_id(db: Session, preferences_id: int):
    """
    Get partner preferences by ID
    
    Purpose: Retrieve specific preference record (admin operations)
    """
    return db.query(PartnerPreferences).filter(PartnerPreferences.id == preferences_id).first()

def get_partner_preferences_by_profile(db: Session, profile_id: int):
    """
    Get all partner preferences for a specific profile
    
    Purpose: Display preferences on profile page
    Note: Returns list (though typically 1 record per profile)
    """
    return db.query(PartnerPreferences).filter(PartnerPreferences.profile_id == profile_id).all()

def update_preferences(db: Session, preferences_id: int, preferences_data: PartnerPreferencesUpdate):
    """
    Update partner preferences (partial update)
    
    Purpose: Allow users to modify their partner requirements
    Use Cases:
    - User changes age range preference
    - User updates location preference (relocation plans)
    - User adjusts star/rasi preferences after astrologer consultation
    """
    db_preferences = db.query(PartnerPreferences).filter(PartnerPreferences.id == preferences_id).first()
    
    if not db_preferences:
        return None
    
    # Update only provided fields
    update_data = preferences_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_preferences, field, value)
    
    db.commit()
    db.refresh(db_preferences)
    return db_preferences

def update_preferences_by_profile_id(db: Session, profile_id: int, preferences_data: PartnerPreferencesUpdate):
    """
    Update partner preferences by profile_id (partial update)
    
    Purpose: Update preferences directly from profile context
    
    Why This is Needed:
    - Simpler API for frontend: no need to fetch preferences_id first
    - Direct profile-based workflow: "Update preferences for profile #123"
    - Reduces API calls: Single call instead of GET + PATCH
    
    Use Cases:
    1. Profile settings page: User updates partner requirements
    2. Onboarding flow: Progressive preference setting
    3. Life changes: User relocates, updates location preference
    4. Age adjustment: User gets older, adjusts age_from/age_to
    5. Career growth: User achieves higher position, updates occupation preference
    
    Example Workflow:
    Frontend has profile_id from session
    → User changes "Age: 25-30" to "Age: 27-32"
    → PATCH /partner-preferences/profile/123 with updated data
    → No need to fetch preferences_id first
    
    Real-World Scenarios:
    - User relocates to USA: Updates location_preference to "USA, Canada"
    - User's age changes: Adjusts age_from/age_to accordingly
    - User consults astrologer: Updates star/rasi preferences
    
    Returns: Updated preferences record or newly created one
    """
    # Get all preferences for this profile
    all_preferences = db.query(PartnerPreferences).filter(
        PartnerPreferences.profile_id == profile_id
    ).all()
    
    # If no preferences exist, create new entry
    if not all_preferences:
        # Convert update data to create data
        update_data = preferences_data.dict(exclude_unset=True)
        update_data['profile_id'] = profile_id
        create_data = PartnerPreferencesCreate(**update_data)
        return create_partner_preferences(db, create_data)
    
    # Use the first preference record
    db_preferences = all_preferences[0]
    
    # If there are duplicates, delete them
    if len(all_preferences) > 1:
        for duplicate in all_preferences[1:]:
            delete_preferences(db, duplicate.id)
    
    # Update only provided fields
    update_data = preferences_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_preferences, field, value)
    
    db.commit()
    db.refresh(db_preferences)
    return db_preferences

def delete_preferences(db: Session, preferences_id: int):
    """
    Delete partner preferences
    
    Purpose: Remove preference data (user wants to reset preferences)
    Note: CASCADE delete will happen automatically if profile is deleted
    """
    db_preferences = db.query(PartnerPreferences).filter(PartnerPreferences.id == preferences_id).first()
    
    if not db_preferences:
        return None
    
    db.delete(db_preferences)
    db.commit()
    return db_preferences

def delete_preferences_by_profile_id(db: Session, profile_id: int):
    """
    Delete partner preferences by profile_id
    
    Purpose: Remove preferences using profile reference
    
    Why This is Needed:
    - Profile-centric deletion: "Remove preferences for profile #123"
    - Simpler frontend logic: no need to fetch preferences_id first
    - Reset flow: User wants to start fresh with preferences
    
    Use Cases:
    1. Reset preferences: User wants to redefine all requirements
    2. Profile cleanup: Remove incomplete preference data
    3. Privacy: User wants to temporarily hide preferences
    
    Returns: Count of deleted records
    """
    db_preferences_records = db.query(PartnerPreferences).filter(
        PartnerPreferences.profile_id == profile_id
    ).all()
    
    if not db_preferences_records:
        return None
    
    deleted_count = 0
    for record in db_preferences_records:
        db.delete(record)
        deleted_count += 1
    
    db.commit()
    return deleted_count

def find_matching_profiles(db: Session, profile_id: int, skip: int = 0, limit: int = 100):
    """
    Find profiles that match user's partner preferences
    
    Purpose: Core matching algorithm - find compatible profiles
    
    Why This is Needed:
    The heart of matrimony platform - automated partner discovery:
    - User sets preferences (age, height, education, etc.)
    - System finds profiles matching those criteria
    - Reduces manual search effort
    - Increases match quality
    
    Matching Logic:
    1. Get user's partner preferences
    2. Query profiles table with those filters
    3. Return matching profiles
    
    Example:
    User preferences:
    - Age: 25-30
    - Height: 160-175 cm
    - Star: Rohini, Ashwini
    - Location: Chennai, Bangalore
    
    System finds profiles meeting ALL criteria
    
    Use Cases:
    - "Show me matches" button on homepage
    - Daily match recommendations
    - Search results page
    
    Note: This is a simplified version. Production would use:
    - Complex scoring algorithm
    - Weighted preferences (some criteria more important)
    - Fuzzy matching (partial matches)
    - Boost recent/active profiles
    
    Returns: List of partner_preferences records that match user's profile
    """
    # Get user's profile first (to match against preferences)
    from ..models.profile import Profile
    user_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    
    if not user_profile:
        return []
    
    # Find partner preferences where user's profile fits the criteria
    query = db.query(PartnerPreferences).filter(PartnerPreferences.profile_id != profile_id)
    
    # Age matching (if user's age is within preference range)
    if user_profile.birth_date:
        from datetime import date
        user_age = (date.today() - user_profile.birth_date).days // 365
        query = query.filter(
            (PartnerPreferences.age_from.is_(None)) | (PartnerPreferences.age_from <= user_age)
        ).filter(
            (PartnerPreferences.age_to.is_(None)) | (PartnerPreferences.age_to >= user_age)
        )
    
    # Height matching (if user's height is within preference range)
    if user_profile.height_cm:
        query = query.filter(
            (PartnerPreferences.height_from.is_(None)) | (PartnerPreferences.height_from <= user_profile.height_cm)
        ).filter(
            (PartnerPreferences.height_to.is_(None)) | (PartnerPreferences.height_to >= user_profile.height_cm)
        )
    
    return query.offset(skip).limit(limit).all()

def get_profiles_seeking_age_range(db: Session, age_from: int, age_to: int, skip: int = 0, limit: int = 100):
    """
    Find preferences looking for specific age range
    
    Purpose: Reverse matching - who's looking for users in age X-Y?
    
    Why This is Needed:
    Sometimes users want to know:
    "Who is looking for someone my age?"
    "Show me profiles seeking 25-30 year olds"
    
    Use Cases:
    - Admin analytics: "How many profiles seek 25-30 age group?"
    - Reverse search: "Who wants someone like me?"
    
    Returns: Preferences with age_from/age_to overlapping given range
    """
    return (
        db.query(PartnerPreferences)
        .filter(
            ((PartnerPreferences.age_from <= age_to) & (PartnerPreferences.age_to >= age_from)) |
            (PartnerPreferences.age_from.is_(None)) |
            (PartnerPreferences.age_to.is_(None))
        )
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_profiles_seeking_height_range(db: Session, height_from: int, height_to: int, skip: int = 0, limit: int = 100):
    """
    Find preferences looking for specific height range
    
    Purpose: Reverse matching - who's looking for users with height X-Y cm?
    
    Why This is Needed:
    Height preference filtering:
    "Show me profiles seeking 160-170 cm partners"
    
    Returns: Preferences with height_from/height_to overlapping given range
    """
    return (
        db.query(PartnerPreferences)
        .filter(
            ((PartnerPreferences.height_from <= height_to) & (PartnerPreferences.height_to >= height_from)) |
            (PartnerPreferences.height_from.is_(None)) |
            (PartnerPreferences.height_to.is_(None))
        )
        .offset(skip)
        .limit(limit)
        .all()
    )
