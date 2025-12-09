from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.partner_preferences import (
    PartnerPreferencesCreate, 
    PartnerPreferencesUpdate, 
    PartnerPreferencesResponse,
    PreferenceOptions
)
from app.crud.partner_preferences import (
    create_partner_preferences, 
    get_preferences_by_id,
    get_partner_preferences_by_profile,
    update_preferences,
    update_preferences_by_profile_id,
    delete_preferences,
    delete_preferences_by_profile_id,
    find_matching_profiles,
    get_profiles_seeking_age_range,
    get_profiles_seeking_height_range
)

router = APIRouter(prefix="/partner-preferences", tags=["partner-preferences"])

@router.post("/", response_model=PartnerPreferencesResponse, status_code=status.HTTP_201_CREATED)
def create_new_partner_preferences(preferences: PartnerPreferencesCreate, db: Session = Depends(get_db)):
    """
    Create partner preferences for a profile
    
    Purpose: Set partner requirements when user fills preference form
    
    Fields Explained:
    - age_from/age_to: Acceptable age range (e.g., 25-30)
    - height_from/height_to: Height range in cm (e.g., 160-175)
    - education_preference: Comma-separated (e.g., "Bachelor's, Master's")
    - occupation_preference: Comma-separated (e.g., "Engineer, Doctor")
    - income_preference: Income range (e.g., "10-20 LPA")
    - star_preference: Astrological stars (e.g., "Rohini, Ashwini")
    - rasi_preference: Zodiac signs (e.g., "Aries, Taurus")
    - location_preference: Locations (e.g., "Chennai, USA")
    """
    return create_partner_preferences(db, preferences)

@router.get("/{preferences_id}", response_model=PartnerPreferencesResponse)
def read_preferences(preferences_id: int, db: Session = Depends(get_db)):
    """
    Get partner preferences by ID
    
    Purpose: Retrieve specific preference record
    Use Case: Admin review, direct access
    """
    db_preferences = get_preferences_by_id(db, preferences_id)
    
    if db_preferences is None:
        raise HTTPException(status_code=404, detail="Partner preferences not found")
    
    return db_preferences

@router.get("/profile/{profile_id}", response_model=list[PartnerPreferencesResponse])
def read_preferences_by_profile(profile_id: int, db: Session = Depends(get_db)):
    """
    Get all partner preferences for a profile
    
    Purpose: Display preferences on profile page
    Returns: List of preference records (typically 1 per profile)
    """
    return get_partner_preferences_by_profile(db, profile_id)

@router.patch("/{preferences_id}", response_model=PartnerPreferencesResponse)
def update_preferences_route(
    preferences_id: int, 
    preferences: PartnerPreferencesUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update partner preferences by preferences_id (partial update)
    
    Purpose: Modify partner requirements
    
    Use Cases:
    1. Age adjustment: User ages, updates age_from/age_to
    2. Location change: User relocates, updates location_preference
    3. Career growth: Updates occupation/income preferences
    4. Astrological consultation: Updates star/rasi preferences
    
    Example Request:
    PATCH /partner-preferences/123
    {
        "age_from": 27,
        "age_to": 32,
        "location_preference": "USA, Canada, UK"
    }
    """
    db_preferences = update_preferences(db, preferences_id, preferences)
    
    if db_preferences is None:
        raise HTTPException(status_code=404, detail="Partner preferences not found")
    
    return db_preferences

@router.patch("/profile/{profile_id}", response_model=PartnerPreferencesResponse)
def update_preferences_by_profile(
    profile_id: int, 
    preferences: PartnerPreferencesUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update partner preferences by profile_id (partial update)
    
    Purpose: Update preferences directly from profile context
    
    Why This Endpoint is Needed:
    
    1. **Simpler Frontend Logic**
       - Frontend stores profile_id in session
       - No need to fetch preferences_id before updating
       - Single API call for updates
    
    2. **Better UX Flow**
       User in profile settings:
       → Goes to "Partner Preferences" section
       → Updates "Age: 25-30" to "Age: 27-32"
       → Clicks "Save"
       → Frontend calls: PATCH /partner-preferences/profile/{profile_id}
       → No intermediate lookup needed
    
    3. **Life Changes**
       - User relocates: Updates location_preference
       - User ages: Adjusts age_from/age_to
       - Career change: Updates occupation_preference
       - Income increase: Updates income_preference
    
    4. **Progressive Preference Setting**
       Initial setup: Basic preferences only
       Later: Add detailed requirements
       Even later: Refine based on experience
    
    Use Cases:
    - Settings page: Update partner requirements
    - Mobile app: Simplified state management
    - Onboarding: Progressive preference completion
    - Admin panel: Modify user preferences
    
    Example Request:
    PATCH /partner-preferences/profile/123
    {
        "age_from": 25,
        "age_to": 30,
        "height_from": 160,
        "height_to": 175,
        "education_preference": "Bachelor's, Master's",
        "location_preference": "Chennai, Bangalore, USA"
    }
    
    Returns: Updated preferences record
    Throws: 404 if profile has no preferences record
    """
    db_preferences = update_preferences_by_profile_id(db, profile_id, preferences)
    
    if db_preferences is None:
        raise HTTPException(
            status_code=404, 
            detail=f"No partner preferences found for profile_id {profile_id}"
        )
    
    return db_preferences

@router.delete("/{preferences_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_preferences_route(preferences_id: int, db: Session = Depends(get_db)):
    """
    Delete partner preferences by preferences_id
    
    Purpose: Remove preference data
    Use Cases:
    - Reset preferences: Start fresh
    - Data cleanup: Remove old preferences
    
    Note: If profile is deleted, preferences auto-delete (CASCADE)
    """
    db_preferences = delete_preferences(db, preferences_id)
    
    if db_preferences is None:
        raise HTTPException(status_code=404, detail="Partner preferences not found")
    
    return None

@router.delete("/profile/{profile_id}", status_code=status.HTTP_200_OK)
def delete_preferences_by_profile(profile_id: int, db: Session = Depends(get_db)):
    """
    Delete partner preferences by profile_id
    
    Purpose: Remove preferences using profile reference
    
    Why This Endpoint is Needed:
    
    1. **Reset Workflow**
       User wants to:
       - Completely redefine preferences
       - Start fresh with new requirements
       - Easier than updating all fields to NULL
    
    2. **Profile Management**
       - User takes break from matrimony search
       - Temporarily remove preferences
       - Re-add later when ready
    
    3. **Admin Operations**
       - Remove incomplete preference data
       - Cleanup during profile review
    
    Use Cases:
    - User: "Reset my partner preferences"
    - Profile cleanup: Remove incomplete data
    - Admin moderation: Remove inappropriate preferences
    
    Example Request:
    DELETE /partner-preferences/profile/123
    
    Returns: 
    {
        "message": "Deleted 1 preference record(s) for profile_id 123",
        "profile_id": 123,
        "deleted_count": 1
    }
    
    Throws: 404 if profile has no preferences record
    """
    deleted_count = delete_preferences_by_profile_id(db, profile_id)
    
    if deleted_count is None:
        raise HTTPException(
            status_code=404, 
            detail=f"No partner preferences found for profile_id {profile_id}"
        )
    
    return {
        "message": f"Deleted {deleted_count} preference record(s) for profile_id {profile_id}",
        "profile_id": profile_id,
        "deleted_count": deleted_count
    }

# ==================== UTILITY ENDPOINTS ====================

@router.get("/options/list", response_model=PreferenceOptions)
def get_preference_options():
    """
    Get standard preference options for UI dropdowns
    
    Purpose: Provide consistent options for frontend forms
    
    Why This is Needed:
    - Frontend needs standardized dropdown values
    - Consistent user experience across app
    - Easy to maintain options in one place
    
    Use Cases:
    - Populate preference form dropdowns
    - Auto-complete suggestions
    - Validation reference
    
    Returns:
    {
        "education_options": ["Bachelor's", "Master's", ...],
        "occupation_options": ["Engineer", "Doctor", ...],
        "income_options": ["5-10 LPA", "10-15 LPA", ...],
        "location_options": ["Chennai", "Bangalore", ...]
    }
    
    Frontend Usage:
    - Load options on form mount
    - Cache for session duration
    - Use for dropdown population
    """
    return PreferenceOptions()

# ==================== MATCHING ENDPOINTS ====================

@router.get("/matches/{profile_id}", response_model=list[PartnerPreferencesResponse])
def get_matching_profiles(
    profile_id: int, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Find profiles that match user's partner preferences
    
    Purpose: Core matching feature - automated partner discovery
    
    Why This is Needed:
    The most important feature of matrimony platform:
    - User sets preferences (age, height, education, etc.)
    - System automatically finds compatible profiles
    - Saves time compared to manual search
    - Increases likelihood of finding suitable match
    
    Matching Algorithm:
    1. Get user's partner preferences
    2. Query profiles where user's profile fits their criteria
    3. Return matching preference records
    4. Frontend fetches corresponding profile details
    
    Example Flow:
    User (Profile #123):
    - Age: 28
    - Height: 165 cm
    - Education: Master's
    - Location: Chennai
    
    System finds partner_preferences where:
    - age_from <= 28 AND age_to >= 28
    - height_from <= 165 AND height_to >= 165
    - education_preference contains "Master's"
    - location_preference contains "Chennai"
    
    Use Cases:
    - "Show me matches" button on homepage
    - Daily match recommendations email
    - Search results page
    - Match percentage calculation
    
    Example Request:
    GET /partner-preferences/matches/123?skip=0&limit=20
    
    Returns: First 20 matching partner preferences
    
    Note: This is simplified. Production would include:
    - Weighted scoring (some criteria more important)
    - Fuzzy matching (partial matches)
    - Boost premium/verified profiles
    - Filter by mutual interest
    - Exclude blocked/ignored profiles
    """
    return find_matching_profiles(db, profile_id, skip, limit)

@router.get("/search/age-range", response_model=list[PartnerPreferencesResponse])
def search_by_age_range(
    age_from: int, 
    age_to: int, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Find preferences looking for specific age range
    
    Purpose: Reverse matching - who's looking for users aged X-Y?
    
    Why This is Needed:
    Sometimes users want to know:
    - "Who is looking for someone my age?"
    - "Show me profiles seeking 25-30 year olds"
    - Admin analytics: "How many profiles seek age 28-32?"
    
    Use Cases:
    - Reverse search: "Who wants someone like me?"
    - Admin dashboard: Preference distribution analytics
    - Market research: Popular age ranges
    
    Example Request:
    GET /partner-preferences/search/age-range?age_from=25&age_to=30
    
    Returns: Preferences with age_from/age_to overlapping 25-30 range
    """
    return get_profiles_seeking_age_range(db, age_from, age_to, skip, limit)

@router.get("/search/height-range", response_model=list[PartnerPreferencesResponse])
def search_by_height_range(
    height_from: int, 
    height_to: int, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Find preferences looking for specific height range
    
    Purpose: Reverse matching - who's looking for users with height X-Y cm?
    
    Why This is Needed:
    Height preference analytics:
    - "Show me profiles seeking 160-170 cm partners"
    - Admin analytics: Popular height preferences
    
    Use Cases:
    - Reverse height search
    - Admin dashboard: Height preference distribution
    - Market insights: Height trends
    
    Example Request:
    GET /partner-preferences/search/height-range?height_from=160&height_to=175
    
    Returns: Preferences with height_from/height_to overlapping 160-175 range
    """
    return get_profiles_seeking_height_range(db, height_from, height_to, skip, limit)
