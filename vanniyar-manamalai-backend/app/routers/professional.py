from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.professional import (
    ProfessionalDetailsCreate, 
    ProfessionalDetailsUpdate, 
    ProfessionalDetailsResponse,
    ProfessionalOptions,
    ProfessionalSummary
)
from app.crud.professional import (
    create_professional, 
    get_professional_by_id,
    get_professional_by_profile,
    update_professional,
    update_professional_by_profile_id,
    delete_professional,
    delete_professional_by_profile_id,
    get_profiles_by_education,
    get_profiles_by_occupation,
    get_profiles_by_employment_type,
    get_profiles_by_work_location,
    get_profiles_with_advanced_degrees
)

router = APIRouter(prefix="/professional", tags=["professional"])

@router.post("/", response_model=ProfessionalDetailsResponse, status_code=status.HTTP_201_CREATED)
def create_new_professional(professional: ProfessionalDetailsCreate, db: Session = Depends(get_db)):
    """
    Create professional details for a profile
    
    Purpose: Add education and employment information during profile creation
    
    Fields Explained:
    - education: Primary qualification (e.g., "Bachelor's in Engineering")
    - education_optional: Additional degrees (e.g., "MBA", "PhD", "CA")
    - employment_type: Status (Employed/Self-employed/Business/Unemployed)
    - occupation: Profession (Engineer/Doctor/Teacher/etc.)
    - company_name: Employer/organization
    - annual_income: Income range (e.g., "10-15 LPA")
    - work_location: City/country (Chennai/Bangalore/USA)
    """
    return create_professional(db, professional)

@router.get("/{professional_id}", response_model=ProfessionalDetailsResponse)
def read_professional(professional_id: int, db: Session = Depends(get_db)):
    """
    Get professional details by ID
    
    Purpose: Retrieve specific professional record
    Use Case: Admin review, direct access
    """
    db_professional = get_professional_by_id(db, professional_id)
    
    if db_professional is None:
        raise HTTPException(status_code=404, detail="Professional details not found")
    
    return db_professional

@router.get("/profile/{profile_id}", response_model=list[ProfessionalDetailsResponse])
def read_professional_by_profile(profile_id: int, db: Session = Depends(get_db)):
    """
    Get all professional details for a profile
    
    Purpose: Display professional info on profile page
    Returns: List of professional records (typically 1 per profile)
    """
    return get_professional_by_profile(db, profile_id)

@router.patch("/{professional_id}", response_model=ProfessionalDetailsResponse)
def update_professional_route(
    professional_id: int, 
    professional: ProfessionalDetailsUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update professional details by professional_id (partial update)
    
    Purpose: Modify education and employment information
    
    Use Cases:
    1. Job change: New company, location, salary
    2. Career progression: Promotion, new role
    3. Educational advancement: Completed MBA/PhD
    4. Business start: Changed employment_type to "Business"
    5. Relocation: Updated work_location
    
    Example Request:
    PATCH /professional/123
    {
        "company_name": "Google",
        "work_location": "Bangalore",
        "annual_income": "20-30 LPA"
    }
    """
    db_professional = update_professional(db, professional_id, professional)
    
    if db_professional is None:
        raise HTTPException(status_code=404, detail="Professional details not found")
    
    return db_professional

@router.patch("/profile/{profile_id}", response_model=ProfessionalDetailsResponse)
def update_professional_by_profile(
    profile_id: int, 
    professional: ProfessionalDetailsUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update professional details by profile_id (partial update)
    
    Purpose: Update professional info directly from profile context
    
    Why This Endpoint is Needed:
    
    1. **Simpler Frontend Logic**
       - Frontend stores profile_id in session
       - No need to fetch professional_id before updating
       - Single API call for updates
    
    2. **Better UX Flow**
       User in profile settings:
       → Goes to "Career Details" section
       → Updates job/company information
       → Clicks "Save"
       → Frontend calls: PATCH /professional/profile/{profile_id}
       → No intermediate lookup needed
    
    3. **Real-World Career Changes**
       - Job switch: New company, location, salary
       - Promotion: Updated occupation/role
       - Additional degree: Completed MBA/PhD
       - Business start: Changed employment status
       - Relocation: Moved to different city/country
    
    4. **Progressive Profile Completion**
       Initial setup: Basic education info
       Later: Add employment details
       Even later: Update with career progression
    
    Use Cases:
    - Profile edit page: Update career section
    - Job change notification: "Joined new company"
    - Educational milestone: "Completed MBA"
    - Location change: "Relocated to USA"
    - Income update: "Salary increased"
    
    Example Request:
    PATCH /professional/profile/123
    {
        "company_name": "TCS",
        "occupation": "Software Engineer",
        "work_location": "Chennai",
        "annual_income": "10-15 LPA",
        "education_optional": "MBA"
    }
    
    Returns: Updated professional record
    Throws: 404 if profile has no professional record
    """
    db_professional = update_professional_by_profile_id(db, profile_id, professional)
    
    if db_professional is None:
        raise HTTPException(
            status_code=404, 
            detail=f"No professional details found for profile_id {profile_id}"
        )
    
    return db_professional

@router.delete("/{professional_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_professional_route(professional_id: int, db: Session = Depends(get_db)):
    """
    Delete professional details by professional_id
    
    Purpose: Remove professional data
    Use Cases:
    - Data cleanup: Remove old career info
    - Privacy: Hide employment details
    
    Note: If profile is deleted, professional details auto-delete (CASCADE)
    """
    db_professional = delete_professional(db, professional_id)
    
    if db_professional is None:
        raise HTTPException(status_code=404, detail="Professional details not found")
    
    return None

@router.delete("/profile/{profile_id}", status_code=status.HTTP_200_OK)
def delete_professional_by_profile(profile_id: int, db: Session = Depends(get_db)):
    """
    Delete professional details by profile_id
    
    Purpose: Remove professional data using profile reference
    
    Why This Endpoint is Needed:
    
    1. **Privacy Management**
       User wants to:
       - Temporarily hide employment info
       - Remove company name (privacy concern)
       - Delete career details during job search
    
    2. **Profile Cleanup**
       - Remove incomplete professional data
       - Delete outdated information
       - Reset before adding new details
    
    3. **Career Transition**
       - Between jobs: Delete old info
       - Career change: Clear previous details
       - Student to employed: Remove old status
    
    Use Cases:
    - User: "Hide my employment information"
    - Profile cleanup: Remove incomplete data
    - Career transition: Delete before update
    
    Example Request:
    DELETE /professional/profile/123
    
    Returns: 
    {
        "message": "Deleted 1 professional record(s) for profile_id 123",
        "profile_id": 123,
        "deleted_count": 1
    }
    
    Throws: 404 if profile has no professional record
    """
    deleted_count = delete_professional_by_profile_id(db, profile_id)
    
    if deleted_count is None:
        raise HTTPException(
            status_code=404, 
            detail=f"No professional details found for profile_id {profile_id}"
        )
    
    return {
        "message": f"Deleted {deleted_count} professional record(s) for profile_id {profile_id}",
        "profile_id": profile_id,
        "deleted_count": deleted_count
    }

# ==================== UTILITY ENDPOINTS ====================

@router.get("/options/list", response_model=ProfessionalOptions)
def get_professional_options():
    """
    Get standard professional options for UI dropdowns
    
    Purpose: Provide consistent options for frontend forms
    
    Why This is Needed:
    - Frontend needs standardized dropdown values
    - Consistent user experience across app
    - Easy to maintain options centrally
    
    Use Cases:
    - Populate professional form dropdowns
    - Auto-complete suggestions
    - Validation reference
    
    Returns:
    {
        "education_options": ["Bachelor's", "Master's", ...],
        "employment_type_options": ["Employed", "Business", ...],
        "occupation_options": ["Engineer", "Doctor", ...],
        "income_options": ["5-10 LPA", "10-15 LPA", ...],
        "location_options": ["Chennai", "Bangalore", ...]
    }
    
    Frontend Usage:
    - Load options on form mount
    - Cache for session duration
    - Use for dropdown population
    """
    return ProfessionalOptions()

@router.get("/profile/{profile_id}/summary", response_model=ProfessionalSummary)
def get_professional_summary(profile_id: int, db: Session = Depends(get_db)):
    """
    Get computed professional summary
    
    Purpose: Provide display-friendly summary for UI
    
    Why This is Needed:
    - Frontend doesn't need to format strings
    - Consistent summary format across app
    - Used in profile cards, match results
    
    Computed Fields:
    - education_summary: "B.E. + MBA" or "B.Sc."
    - employment_summary: "Employed as Engineer at TCS in Chennai"
    - income_summary: "10-15 LPA" or "Not specified"
    - is_employed: Boolean flag
    - has_advanced_degree: Boolean flag (MBA/PhD/CA/CS)
    
    Use Cases:
    - Profile card display
    - Search results summary
    - Match recommendations
    
    Example Response:
    {
        "education_summary": "Bachelor's in Engineering + MBA",
        "employment_summary": "Employed as Software Engineer at Google in Bangalore",
        "income_summary": "20-30 LPA",
        "is_employed": true,
        "has_advanced_degree": true
    }
    """
    professional_records = get_professional_by_profile(db, profile_id)
    
    if not professional_records:
        raise HTTPException(
            status_code=404, 
            detail=f"No professional details found for profile_id {profile_id}"
        )
    
    # Get first record (should only be one per profile)
    professional = professional_records[0]
    
    # Convert to response model first
    professional_response = ProfessionalDetailsResponse.from_orm(professional)
    
    return ProfessionalSummary.from_professional_details(professional_response)

# ==================== SEARCH/MATCHING ENDPOINTS ====================

@router.get("/search/by-education/{education}", response_model=list[ProfessionalDetailsResponse])
def search_by_education(
    education: str, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Find profiles by education qualification
    
    Purpose: Matching algorithm - filter by education level
    
    Why This is Needed:
    Educational compatibility is important:
    - Users prefer similar education backgrounds
    - Family expectations about partner's education
    - Common search filter in matrimony
    
    Search is case-insensitive and uses partial matching:
    - "Engineer" matches "Bachelor's in Engineering"
    - "Medical" matches "Medical Degree"
    - "Master" matches "Master's Degree"
    
    Use Cases:
    - "Show me Engineering graduates"
    - "Find profiles with Bachelor's Degree"
    - Partner preference: education_preference matching
    
    Example Request:
    GET /professional/search/by-education/Engineering?skip=0&limit=20
    
    Returns: First 20 profiles with education matching "Engineering"
    """
    return get_profiles_by_education(db, education, skip, limit)

@router.get("/search/by-occupation/{occupation}", response_model=list[ProfessionalDetailsResponse])
def search_by_occupation(
    occupation: str, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Find profiles by occupation
    
    Purpose: Matching algorithm - filter by profession
    
    Why This is Needed:
    Occupation matters in matrimony:
    - Users may prefer specific professions
    - Family prestige considerations (Doctor/Engineer)
    - Career compatibility (similar work hours/stress)
    
    Search is case-insensitive and uses partial matching:
    - "Engineer" matches "Software Engineer", "Civil Engineer"
    - "Doctor" matches all medical professionals
    
    Use Cases:
    - "Show me Engineers"
    - "Find Doctors/Medical professionals"
    - Partner preference: occupation_preference matching
    
    Example Request:
    GET /professional/search/by-occupation/Engineer?skip=0&limit=20
    
    Returns: First 20 profiles with occupation matching "Engineer"
    """
    return get_profiles_by_occupation(db, occupation, skip, limit)

@router.get("/search/by-employment-type/{employment_type}", response_model=list[ProfessionalDetailsResponse])
def search_by_employment_type(
    employment_type: str, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Find profiles by employment type
    
    Purpose: Matching algorithm - filter by employment status
    
    Why This is Needed:
    Employment status affects lifestyle and compatibility:
    - Employed: Stable income, fixed schedule
    - Self-employed: Flexibility, variable income
    - Business: Entrepreneurial, higher risk/reward
    - Unemployed: May need financially stable partner
    
    Valid Values:
    - Employed
    - Self-employed
    - Business
    - Unemployed
    - Student
    - Retired
    
    Use Cases:
    - "Show me employed profiles"
    - "Find business owners"
    - Filter by employment stability
    
    Example Request:
    GET /professional/search/by-employment-type/Employed?skip=0&limit=20
    
    Returns: First 20 employed profiles
    """
    return get_profiles_by_employment_type(db, employment_type, skip, limit)

@router.get("/search/by-location/{work_location}", response_model=list[ProfessionalDetailsResponse])
def search_by_work_location(
    work_location: str, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Find profiles by work location
    
    Purpose: Geographic matching - filter by work city/country
    
    Why This is Needed:
    Location is critical for post-marriage life:
    - Users prefer local matches (same city)
    - International location consideration (USA/UK)
    - Relocation feasibility
    - Family proximity
    
    Search is case-insensitive and uses partial matching:
    - "Chennai" matches "Chennai", "Chennai, India"
    - "USA" matches all US locations
    - "Bangalore" matches "Bengaluru", "Bangalore"
    
    Use Cases:
    - "Show me profiles working in Chennai"
    - "Find profiles in USA"
    - Location-based partner preference
    
    Example Request:
    GET /professional/search/by-location/Chennai?skip=0&limit=20
    
    Returns: First 20 profiles working in Chennai
    """
    return get_profiles_by_work_location(db, work_location, skip, limit)

@router.get("/search/advanced-degrees", response_model=list[ProfessionalDetailsResponse])
def search_advanced_degrees(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Find profiles with advanced/additional qualifications
    
    Purpose: Filter highly educated candidates
    
    Why This is Needed:
    Additional qualifications are highly valued:
    - MBA: Business acumen, higher earning potential
    - PhD: Research/academic excellence
    - CA/CS: Professional certifications
    - M.Tech/M.E.: Advanced engineering expertise
    
    Signals:
    - Career ambition and dedication
    - Higher education commitment
    - Potential for career growth
    - Family prestige considerations
    
    Use Cases:
    - "Show me profiles with MBA"
    - "Find PhD holders"
    - Partner preference: prefer advanced degrees
    - Premium profile filtering
    
    Example Request:
    GET /professional/search/advanced-degrees?skip=0&limit=20
    
    Returns: First 20 profiles with education_optional populated
    
    Note: Returns profiles where education_optional field is not empty
    """
    return get_profiles_with_advanced_degrees(db, skip, limit)
