from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..models.family import FamilyDetails
from ..schemas.family import FamilyDetailsCreate, FamilyDetailsUpdate, FamilySummary
from fastapi import HTTPException

def create_family(db: Session, family_data: FamilyDetailsCreate):
    """
    Create new family details for a profile
    
    Purpose: Store family background when user completes profile
    """
    try:
        db_family = FamilyDetails(**family_data.dict())
        db.add(db_family)
        db.commit()
        db.refresh(db_family)
        return db_family
    except IntegrityError as e:
        db.rollback()
        if "foreign key constraint" in str(e).lower():
            raise HTTPException(status_code=400, detail="Invalid profile_id: Profile does not exist")
        raise HTTPException(status_code=400, detail="Database integrity error")

def get_family_by_id(db: Session, family_id: int):
    """
    Get family details by ID
    
    Purpose: Retrieve specific family record (admin operations)
    """
    return db.query(FamilyDetails).filter(FamilyDetails.id == family_id).first()

def get_family_by_profile(db: Session, profile_id: int):
    """
    Get all family details for a specific profile
    
    Purpose: Display family info on profile page
    Note: Returns list (though typically 1 record per profile)
    """
    return db.query(FamilyDetails).filter(FamilyDetails.profile_id == profile_id).all()

def update_family(db: Session, family_id: int, family_data: FamilyDetailsUpdate):
    """
    Update family details (partial update)
    
    Purpose: Allow users to modify family information
    Use Cases:
    - Update parent occupation changes
    - Update sibling marriage status
    - Add family description
    """
    db_family = db.query(FamilyDetails).filter(FamilyDetails.id == family_id).first()
    
    if not db_family:
        return None
    
    # Update only provided fields
    update_data = family_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_family, field, value)
    
    db.commit()
    db.refresh(db_family)
    return db_family

def update_family_by_profile_id(db: Session, profile_id: int, family_data: FamilyDetailsUpdate):
    """
    Update family details by profile_id (partial update)
    
    Purpose: Update family info directly from profile context
    
    Why This is Needed:
    - Simpler API for frontend: no need to fetch family_id first
    - Direct profile-based workflow: "Update family for profile #123"
    - Reduces API calls: Single call instead of GET + PATCH
    
    Use Cases:
    1. Profile edit page: User updates family section
    2. Onboarding flow: Progressive profile completion
    3. Sibling marriage update: Brother/sister got married
    4. Parent occupation change: Father retired, mother started working
    
    Example Workflow:
    Frontend has profile_id from session
    → User edits "Brothers: 2, Married Brothers: 1"
    → PATCH /family/profile/123 with updated data
    → No need to fetch family_id first
    
    Returns: Updated family record or None if not found
    """
    db_family = db.query(FamilyDetails).filter(
        FamilyDetails.profile_id == profile_id
    ).first()
    
    if not db_family:
        return None
    
    # Update only provided fields
    update_data = family_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_family, field, value)
    
    db.commit()
    db.refresh(db_family)
    return db_family

def delete_family(db: Session, family_id: int):
    """
    Delete family details
    
    Purpose: Remove family data (user privacy request or data cleanup)
    Note: CASCADE delete will happen automatically if profile is deleted
    """
    db_family = db.query(FamilyDetails).filter(FamilyDetails.id == family_id).first()
    
    if not db_family:
        return None
    
    db.delete(db_family)
    db.commit()
    return db_family

def delete_family_by_profile_id(db: Session, profile_id: int):
    """
    Delete family details by profile_id
    
    Purpose: Remove family data using profile reference
    
    Why This is Needed:
    - Profile-centric deletion: "Remove family info for profile #123"
    - Simpler frontend logic: no need to fetch family_id first
    - Privacy requests: User wants to hide family details
    
    Use Cases:
    1. User privacy request: "Hide my family information"
    2. Profile cleanup: Remove incomplete family data
    3. Admin moderation: Remove inappropriate family info
    
    Returns: Count of deleted records
    """
    db_family_records = db.query(FamilyDetails).filter(
        FamilyDetails.profile_id == profile_id
    ).all()
    
    if not db_family_records:
        return None
    
    deleted_count = 0
    for record in db_family_records:
        db.delete(record)
        deleted_count += 1
    
    db.commit()
    return deleted_count

def get_profiles_by_family_status(db: Session, family_status: str, skip: int = 0, limit: int = 100):
    """
    Find profiles by family economic status
    
    Purpose: Matching algorithm - find profiles from similar economic background
    
    Why This is Needed:
    In matrimony, economic compatibility is important:
    - Users prefer partners from similar economic background
    - Reduces lifestyle mismatches post-marriage
    - Common filter in advanced search
    
    Use Cases:
    - "Show me profiles from Middle Class families"
    - "Find Rich/Elite family profiles"
    
    Returns: List of family details matching status
    """
    return (
        db.query(FamilyDetails)
        .filter(FamilyDetails.family_status == family_status)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_profiles_by_family_type(db: Session, family_type: str, skip: int = 0, limit: int = 100):
    """
    Find profiles by family structure type
    
    Purpose: Matching algorithm - find profiles from similar family structure
    
    Why This is Needed:
    Family structure affects post-marriage lifestyle:
    - Joint family: Living with parents/relatives
    - Nuclear family: Independent living
    - Extended family: Larger family network
    
    Use Cases:
    - User prefers nuclear family background
    - User comfortable with joint family system
    
    Returns: List of family details matching type
    """
    return (
        db.query(FamilyDetails)
        .filter(FamilyDetails.family_type == family_type)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_profiles_with_unmarried_siblings(db: Session, skip: int = 0, limit: int = 100):
    """
    Find profiles with unmarried siblings
    
    Purpose: Special matching case - parents may want to arrange multiple marriages
    
    Why This is Needed:
    In Tamil/Indian culture:
    - Families with multiple unmarried children may want to find families with similar situation
    - Potential for double/multiple alliance (e.g., brother of groom with sister of bride)
    - Common practice in traditional matrimony
    
    Use Cases:
    - "Find families with unmarried brothers/sisters"
    - Double alliance matching
    
    Calculation:
    Unmarried siblings = (brothers - Married_brothers) + (sisters - Married_sisters)
    
    Returns: Profiles where unmarried siblings > 0
    """
    return (
        db.query(FamilyDetails)
        .filter(
            (FamilyDetails.brothers - FamilyDetails.Married_brothers + 
             FamilyDetails.sisters - FamilyDetails.Married_sisters) > 0
        )
        .offset(skip)
        .limit(limit)
        .all()
    )
