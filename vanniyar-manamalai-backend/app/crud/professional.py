from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..models.professional import ProfessionalDetails
from ..schemas.professional import ProfessionalDetailsCreate, ProfessionalDetailsUpdate
from fastapi import HTTPException

def create_professional(db: Session, professional_data: ProfessionalDetailsCreate):
    """
    Create new professional details for a profile
    
    Purpose: Store education and employment info when user completes profile
    """
    try:
        db_professional = ProfessionalDetails(**professional_data.dict())
        db.add(db_professional)
        db.commit()
        db.refresh(db_professional)
        return db_professional
    except IntegrityError as e:
        db.rollback()
        if "foreign key constraint" in str(e).lower():
            raise HTTPException(status_code=400, detail="Invalid profile_id: Profile does not exist")
        raise HTTPException(status_code=400, detail="Database integrity error")

def get_professional_by_id(db: Session, professional_id: int):
    """
    Get professional details by ID
    
    Purpose: Retrieve specific professional record (admin operations)
    """
    return db.query(ProfessionalDetails).filter(ProfessionalDetails.id == professional_id).first()

def get_professional_by_profile(db: Session, profile_id: int):
    """
    Get all professional details for a specific profile
    
    Purpose: Display professional info on profile page
    Note: Returns list (though typically 1 record per profile)
    """
    return db.query(ProfessionalDetails).filter(ProfessionalDetails.profile_id == profile_id).all()

def update_professional(db: Session, professional_id: int, professional_data: ProfessionalDetailsUpdate):
    """
    Update professional details (partial update)
    
    Purpose: Allow users to modify their professional information
    Use Cases:
    - Job change: Update company_name, work_location
    - Promotion: Update occupation (e.g., "Engineer" → "Senior Engineer")
    - Salary hike: Update annual_income
    - Additional qualification: Add education_optional (e.g., completed MBA)
    - Career change: Update employment_type, occupation
    """
    db_professional = db.query(ProfessionalDetails).filter(ProfessionalDetails.id == professional_id).first()
    
    if not db_professional:
        return None
    
    # Update only provided fields
    update_data = professional_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_professional, field, value)
    
    db.commit()
    db.refresh(db_professional)
    return db_professional

def update_professional_by_profile_id(db: Session, profile_id: int, professional_data: ProfessionalDetailsUpdate):
    """
    Update professional details by profile_id (partial update)
    
    Purpose: Update professional info directly from profile context
    
    Why This is Needed:
    - Simpler API for frontend: no need to fetch professional_id first
    - Direct profile-based workflow: "Update career info for profile #123"
    - Reduces API calls: Single call instead of GET + PATCH
    
    Use Cases:
    1. Profile edit page: User updates career section
    2. Job change: New company, location, salary
    3. Career progression: Promotion, role change
    4. Educational advancement: Completed MBA/PhD
    5. Employment status change: Employed → Self-employed
    
    Example Workflow:
    Frontend has profile_id from session
    → User gets new job: Updates company_name, work_location, annual_income
    → PATCH /professional/profile/123 with updated data
    → No need to fetch professional_id first
    
    Real-World Scenarios:
    - User switches jobs: "Joined Google in Bangalore, 20-30 LPA"
    - User completes MBA: Adds education_optional = "MBA"
    - User starts business: Changes employment_type to "Business"
    - User relocates: Updates work_location from "Chennai" to "USA"
    
    Returns: Updated professional record or None if not found
    """
    db_professional = db.query(ProfessionalDetails).filter(
        ProfessionalDetails.profile_id == profile_id
    ).first()
    
    if not db_professional:
        return None
    
    # Update only provided fields
    update_data = professional_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_professional, field, value)
    
    db.commit()
    db.refresh(db_professional)
    return db_professional

def delete_professional(db: Session, professional_id: int):
    """
    Delete professional details
    
    Purpose: Remove professional data (user privacy request or data cleanup)
    Note: CASCADE delete will happen automatically if profile is deleted
    """
    db_professional = db.query(ProfessionalDetails).filter(ProfessionalDetails.id == professional_id).first()
    
    if not db_professional:
        return None
    
    db.delete(db_professional)
    db.commit()
    return db_professional

def delete_professional_by_profile_id(db: Session, profile_id: int):
    """
    Delete professional details by profile_id
    
    Purpose: Remove professional data using profile reference
    
    Why This is Needed:
    - Profile-centric deletion: "Remove career info for profile #123"
    - Simpler frontend logic: no need to fetch professional_id first
    - Privacy requests: User wants to hide professional details
    
    Use Cases:
    1. Privacy request: "Hide my employment information"
    2. Profile cleanup: Remove incomplete professional data
    3. Career transition: Delete old info before adding new
    
    Returns: Count of deleted records
    """
    db_professional_records = db.query(ProfessionalDetails).filter(
        ProfessionalDetails.profile_id == profile_id
    ).all()
    
    if not db_professional_records:
        return None
    
    deleted_count = 0
    for record in db_professional_records:
        db.delete(record)
        deleted_count += 1
    
    db.commit()
    return deleted_count

def get_profiles_by_education(db: Session, education: str, skip: int = 0, limit: int = 100):
    """
    Find profiles by education qualification
    
    Purpose: Matching algorithm - find profiles with specific education
    
    Why This is Needed:
    Educational compatibility is important in matrimony:
    - Users prefer partners with similar education level
    - Common filter in partner preferences
    - Cultural expectations (e.g., "prefer engineering graduate")
    
    Use Cases:
    - "Show me profiles with Bachelor's Degree"
    - "Find Engineering graduates"
    - Partner preference matching
    
    Returns: Professional details matching education
    """
    return (
        db.query(ProfessionalDetails)
        .filter(ProfessionalDetails.education.ilike(f"%{education}%"))
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_profiles_by_occupation(db: Session, occupation: str, skip: int = 0, limit: int = 100):
    """
    Find profiles by occupation
    
    Purpose: Matching algorithm - find profiles with specific profession
    
    Why This is Needed:
    Occupation compatibility matters:
    - Users may prefer specific professions (Engineer, Doctor, etc.)
    - Family expectations about partner's career
    - Common search filter
    
    Use Cases:
    - "Show me Engineers"
    - "Find Doctors/Medical professionals"
    - Partner preference: occupation_preference
    
    Returns: Professional details matching occupation
    """
    return (
        db.query(ProfessionalDetails)
        .filter(ProfessionalDetails.occupation.ilike(f"%{occupation}%"))
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_profiles_by_employment_type(db: Session, employment_type: str, skip: int = 0, limit: int = 100):
    """
    Find profiles by employment type
    
    Purpose: Matching algorithm - filter by employment status
    
    Why This is Needed:
    Employment status affects lifestyle:
    - Employed: Stable income, fixed work hours
    - Self-employed: Flexible, variable income
    - Business: Entrepreneurial, high risk/reward
    - Unemployed: May need partner with income
    
    Use Cases:
    - "Show me employed profiles"
    - "Find business owners"
    - Filter unemployed candidates
    
    Returns: Professional details matching employment type
    """
    return (
        db.query(ProfessionalDetails)
        .filter(ProfessionalDetails.employment_type == employment_type)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_profiles_by_work_location(db: Session, work_location: str, skip: int = 0, limit: int = 100):
    """
    Find profiles by work location
    
    Purpose: Geographic matching - find profiles working in specific city/country
    
    Why This is Needed:
    Location is critical for matrimony:
    - Long-distance relationships challenging post-marriage
    - Users prefer local matches
    - International relocation consideration (e.g., USA, UK)
    
    Use Cases:
    - "Show me profiles working in Chennai"
    - "Find profiles in USA"
    - Location-based partner preference
    
    Returns: Professional details matching work location
    """
    return (
        db.query(ProfessionalDetails)
        .filter(ProfessionalDetails.work_location.ilike(f"%{work_location}%"))
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_profiles_with_advanced_degrees(db: Session, skip: int = 0, limit: int = 100):
    """
    Find profiles with advanced/additional qualifications
    
    Purpose: Filter highly educated candidates
    
    Why This is Needed:
    Additional qualifications signal:
    - Higher education commitment
    - Career ambition
    - Earning potential
    - Family prestige considerations
    
    Common advanced degrees in India:
    - MBA, PhD, M.Tech, M.E.
    - CA (Chartered Accountant)
    - CS (Company Secretary)
    
    Use Cases:
    - "Show me profiles with MBA"
    - "Find PhD holders"
    - Partner preference: prefer higher education
    
    Returns: Profiles with education_optional field populated
    """
    return (
        db.query(ProfessionalDetails)
        .filter(ProfessionalDetails.education_optional.isnot(None))
        .filter(ProfessionalDetails.education_optional != "")
        .offset(skip)
        .limit(limit)
        .all()
    )
