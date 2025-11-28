from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.family import (
    FamilyDetailsCreate, 
    FamilyDetailsUpdate, 
    FamilyDetailsResponse,
    FamilySummary
)
from app.crud.family import (
    create_family, 
    get_family_by_id,
    get_family_by_profile,
    update_family,
    update_family_by_profile_id,
    delete_family,
    delete_family_by_profile_id,
    get_profiles_by_family_status,
    get_profiles_by_family_type,
    get_profiles_with_unmarried_siblings
)

router = APIRouter(prefix="/family", tags=["family"])

@router.post("/", response_model=FamilyDetailsResponse, status_code=status.HTTP_201_CREATED)
def create_new_family(family: FamilyDetailsCreate, db: Session = Depends(get_db)):
    """
    Create family details for a profile
    
    Purpose: Add family background information during profile creation/completion
    Required: profile_id
    Optional: All other fields (can be filled progressively)
    """
    return create_family(db, family)

@router.get("/{family_id}", response_model=FamilyDetailsResponse)
def read_family(family_id: int, db: Session = Depends(get_db)):
    """
    Get family details by ID
    
    Purpose: Retrieve specific family record
    Use Case: Admin review, direct access
    """
    db_family = get_family_by_id(db, family_id)
    
    if db_family is None:
        raise HTTPException(status_code=404, detail="Family details not found")
    
    return db_family

@router.get("/profile/{profile_id}", response_model=list[FamilyDetailsResponse])
def read_family_by_profile(profile_id: int, db: Session = Depends(get_db)):
    """
    Get all family details for a profile
    
    Purpose: Display family info on profile page
    Returns: List of family records (typically 1 per profile)
    """
    return get_family_by_profile(db, profile_id)

@router.patch("/{family_id}", response_model=FamilyDetailsResponse)
def update_family_route(
    family_id: int, 
    family: FamilyDetailsUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update family details by family_id (partial update)
    
    Purpose: Modify family information
    
    Use Cases:
    1. Parent occupation change: Father retired, mother started business
    2. Sibling marriage: Brother/sister got married (increment Married_brothers/sisters)
    3. Add family description: Additional context about family
    4. Update family status: Economic status changed
    
    Example Request:
    PATCH /family/123
    {
        "Married_brothers": 1,
        "father_occupation": "Retired"
    }
    """
    db_family = update_family(db, family_id, family)
    
    if db_family is None:
        raise HTTPException(status_code=404, detail="Family details not found")
    
    return db_family

@router.patch("/profile/{profile_id}", response_model=FamilyDetailsResponse)
def update_family_by_profile(
    profile_id: int, 
    family: FamilyDetailsUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update family details by profile_id (partial update)
    
    Purpose: Update family info directly from profile context
    
    Why This Endpoint is Needed:
    
    1. **Simpler Frontend Logic**
       - Frontend stores profile_id in session
       - No need to fetch family_id before updating
       - Single API call for updates
    
    2. **Better UX Flow**
       User on profile edit page:
       → Sees family section
       → Updates "Brothers: 2, Married: 1"
       → Clicks "Save"
       → Frontend calls: PATCH /family/profile/{profile_id}
       → No intermediate lookup needed
    
    3. **Progressive Profile Completion**
       Initial registration: Basic info only
       Later: Add family details
       Even later: Update as siblings get married
    
    4. **Real-World Scenarios**
       - Sibling marriage update: "My sister got married last week"
       - Parent occupation change: "Father retired this year"
       - Economic status change: "Family moved to upper middle class"
    
    Use Cases:
    - Profile edit page: Update family section
    - Onboarding flow: Add family info after initial registration
    - Mobile app: Simplified state management
    - Admin panel: Modify user family by profile
    
    Example Request:
    PATCH /family/profile/123
    {
        "brothers": 2,
        "Married_brothers": 1,
        "sisters": 1,
        "Married_sisters": 0,
        "family_status": "upper_middle_class"
    }
    
    Returns: Updated family record
    Throws: 404 if profile has no family record
    """
    db_family = update_family_by_profile_id(db, profile_id, family)
    
    if db_family is None:
        raise HTTPException(
            status_code=404, 
            detail=f"No family details found for profile_id {profile_id}"
        )
    
    return db_family

@router.delete("/{family_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_family_route(family_id: int, db: Session = Depends(get_db)):
    """
    Delete family details by family_id
    
    Purpose: Remove family data
    Use Cases:
    - Data cleanup
    - Remove incorrect entry
    
    Note: If profile is deleted, family details auto-delete (CASCADE)
    """
    db_family = delete_family(db, family_id)
    
    if db_family is None:
        raise HTTPException(status_code=404, detail="Family details not found")
    
    return None

@router.delete("/profile/{profile_id}", status_code=status.HTTP_200_OK)
def delete_family_by_profile(profile_id: int, db: Session = Depends(get_db)):
    """
    Delete family details by profile_id
    
    Purpose: Remove family data using profile reference
    
    Why This Endpoint is Needed:
    
    1. **Privacy Compliance**
       User requests: "Hide my family information"
       → DELETE /family/profile/{profile_id}
       → No need to know family_id
    
    2. **Profile Management**
       User wants to:
       - Remove family info temporarily
       - Re-add later with updated details
       - Easier than update with all NULL values
    
    3. **Admin Moderation**
       - Remove inappropriate family info
       - Cleanup during profile review
    
    Use Cases:
    - User privacy request: "Remove my family details"
    - Profile cleanup: Remove incomplete data
    - Admin moderation: Remove inappropriate content
    
    Example Request:
    DELETE /family/profile/123
    
    Returns: 
    {
        "message": "Deleted 1 family record(s) for profile_id 123",
        "profile_id": 123,
        "deleted_count": 1
    }
    
    Throws: 404 if profile has no family record
    """
    deleted_count = delete_family_by_profile_id(db, profile_id)
    
    if deleted_count is None:
        raise HTTPException(
            status_code=404, 
            detail=f"No family details found for profile_id {profile_id}"
        )
    
    return {
        "message": f"Deleted {deleted_count} family record(s) for profile_id {profile_id}",
        "profile_id": profile_id,
        "deleted_count": deleted_count
    }

# ==================== COMPUTED PROPERTIES ====================

@router.get("/profile/{profile_id}/summary", response_model=FamilySummary)
def get_family_summary(profile_id: int, db: Session = Depends(get_db)):
    """
    Get computed family summary (total siblings, unmarried siblings, etc.)
    
    Purpose: Provide calculated statistics for UI display and matching
    
    Why This is Needed:
    - Frontend doesn't need to calculate totals
    - Consistent calculation logic
    - Used in profile cards, matching algorithm
    
    Computed Fields:
    - total_siblings: brothers + sisters
    - total_married_siblings: Married_brothers + Married_sisters
    - unmarried_brothers: brothers - Married_brothers
    - unmarried_sisters: sisters - Married_sisters
    - total_unmarried_siblings: unmarried_brothers + unmarried_sisters
    
    Use Cases:
    - Profile card display: "2 siblings (1 married)"
    - Matching: Find profiles with similar family size
    - Statistics: Family composition analysis
    
    Example Response:
    {
        "total_siblings": 3,
        "total_married_siblings": 1,
        "unmarried_brothers": 1,
        "unmarried_sisters": 1,
        "total_unmarried_siblings": 2
    }
    """
    family_records = get_family_by_profile(db, profile_id)
    
    if not family_records:
        raise HTTPException(
            status_code=404, 
            detail=f"No family details found for profile_id {profile_id}"
        )
    
    # Get first record (should only be one per profile)
    family = family_records[0]
    
    # Convert to response model first
    family_response = FamilyDetailsResponse.from_orm(family)
    
    return FamilySummary.from_family_details(family_response)

# ==================== MATCHING/SEARCH ENDPOINTS ====================

@router.get("/search/by-status/{family_status}", response_model=list[FamilyDetailsResponse])
def search_by_family_status(
    family_status: str, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Find profiles by family economic status
    
    Purpose: Matching algorithm - find compatible economic backgrounds
    
    Why This is Needed:
    Economic compatibility reduces post-marriage conflicts:
    - Similar lifestyle expectations
    - Comparable spending patterns
    - Reduced financial stress
    
    Valid Values:
    - Middle_Class
    - upper_middle_class
    - Rich/Elite
    
    Use Cases:
    - User search: "Show me Middle Class families"
    - Matching algorithm: Filter by economic status
    - Admin analytics: Distribution by economic status
    
    Example:
    GET /family/search/by-status/Middle_Class?skip=0&limit=20
    
    Returns: First 20 profiles from Middle Class families
    """
    return get_profiles_by_family_status(db, family_status, skip, limit)

@router.get("/search/by-type/{family_type}", response_model=list[FamilyDetailsResponse])
def search_by_family_type(
    family_type: str, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Find profiles by family structure type
    
    Purpose: Matching algorithm - find compatible family structures
    
    Why This is Needed:
    Family structure affects lifestyle:
    - Nuclear: Independent living, privacy
    - Joint: Shared responsibilities, less privacy
    - Extended: Larger support network
    
    Valid Values:
    - nuclear
    - joint
    - extended
    
    Use Cases:
    - User preference: "I prefer nuclear family background"
    - Matching: Filter by family type
    - Cultural fit: Traditional vs modern family setup
    
    Example:
    GET /family/search/by-type/nuclear?skip=0&limit=20
    
    Returns: First 20 profiles from nuclear families
    """
    return get_profiles_by_family_type(db, family_type, skip, limit)

@router.get("/search/unmarried-siblings", response_model=list[FamilyDetailsResponse])
def search_unmarried_siblings(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Find profiles with unmarried siblings
    
    Purpose: Special matching case - double/multiple alliance opportunities
    
    Why This is Needed:
    Traditional Tamil/Indian matrimony practice:
    - Families with multiple unmarried children look for similar families
    - Potential for double alliance (e.g., brother-sister exchange)
    - Strengthens family bonds between two families
    
    Calculation:
    Unmarried siblings = (brothers - Married_brothers) + (sisters - Married_sisters)
    
    Use Cases:
    - "Find families with unmarried brothers/sisters"
    - Double alliance matching algorithm
    - Parents with multiple children to marry
    
    Example:
    GET /family/search/unmarried-siblings?skip=0&limit=20
    
    Returns: Profiles with at least 1 unmarried sibling
    
    Real-World Scenario:
    Family A: 2 unmarried sons
    Family B: 2 unmarried daughters
    → Potential for double alliance (both sons marry both daughters)
    """
    return get_profiles_with_unmarried_siblings(db, skip, limit)
