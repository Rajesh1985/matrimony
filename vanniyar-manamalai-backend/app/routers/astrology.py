from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.astrology import (
    AstrologyDetailsCreate, 
    AstrologyDetailsUpdate, 
    AstrologyDetailsResponse,
    STAR_TAMIL_MAP,
    RASI_TAMIL_MAP
)
from ..crud.astrology import (
    create_astrology, 
    get_astrology_by_id,
    get_astrology_by_profile,
    update_astrology,
    delete_astrology,
    update_astrology_by_profile_id,
    delete_astrology_by_profile_id
)

router = APIRouter(prefix="/astrology", tags=["astrology"])

@router.post("/", response_model=AstrologyDetailsResponse, status_code=status.HTTP_201_CREATED)
def create_new_astrology(astrology: AstrologyDetailsCreate, db: Session = Depends(get_db)):
    """
    Create astrology details for a profile
    
    Purpose: Add horoscope information when user uploads horoscope
    Required: profile_id, file_id (UUID of uploaded horoscope file)
    """
    return create_astrology(db, astrology)

@router.get("/{astrology_id}", response_model=AstrologyDetailsResponse)
def read_astrology(astrology_id: int, db: Session = Depends(get_db)):
    """
    Get astrology details by ID
    
    Purpose: Retrieve specific astrology record
    Use Case: Admin review, direct access
    """
    db_astrology = get_astrology_by_id(db, astrology_id)
    
    if db_astrology is None:
        raise HTTPException(status_code=404, detail="Astrology details not found")
    
    return db_astrology

@router.get("/profile/{profile_id}", response_model=list[AstrologyDetailsResponse])
def read_astrology_by_profile(profile_id: int, db: Session = Depends(get_db)):
    """
    Get all astrology details for a profile
    
    Purpose: Display horoscope info on profile page
    Returns: List of astrology records (typically 1 per profile)
    """
    return get_astrology_by_profile(db, profile_id)

@router.patch("/{astrology_id}", response_model=AstrologyDetailsResponse)
def update_astrology_route(
    astrology_id: int, 
    astrology: AstrologyDetailsUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update astrology details (partial update)
    
    Purpose: Modify horoscope information
    
    Why PATCH:
    - Allows partial updates (send only changed fields)
    - Efficient for single field changes
    
    Use Cases:
    1. User corrects star/rasi after astrologer consultation
    2. User uploads new/better horoscope file (update file_id)
    3. Admin adds dosham details after review
    4. User updates birth place information
    
    Example Request:
    PATCH /astrology/123
    {
        "star": "Rohini",
        "rasi": "Taurus"
    }
    
    Only star and rasi will be updated, other fields remain unchanged.
    """
    db_astrology = update_astrology(db, astrology_id, astrology)
    
    if db_astrology is None:
        raise HTTPException(status_code=404, detail="Astrology details not found")
    
    return db_astrology

@router.delete("/{astrology_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_astrology_route(astrology_id: int, db: Session = Depends(get_db)):
    """
    Delete astrology details
    
    Purpose: Remove horoscope data
    Use Cases:
    - User privacy request
    - Data cleanup
    - Remove incorrect entry
    
    Note: If profile is deleted, astrology details auto-delete (CASCADE)
    """
    db_astrology = delete_astrology(db, astrology_id)
    
    if db_astrology is None:
        raise HTTPException(status_code=404, detail="Astrology details not found")
    
    return None

@router.patch("/profile/{profile_id}", response_model=AstrologyDetailsResponse)
def update_astrology_by_profile(
    profile_id: int, 
    astrology: AstrologyDetailsUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update astrology details by profile_id (partial update)
    
    Purpose: Update horoscope directly from profile context
    
    Why This Endpoint is Needed:
    
    1. **Simpler Frontend Logic**
       - Frontend stores profile_id in session/state
       - No need to fetch astrology_id before updating
       - Reduces API complexity
    
    2. **Better UX Flow**
       User on profile edit page:
       → Sees horoscope section
       → Edits star/rasi
       → Clicks "Save"
       → Frontend calls: PATCH /astrology/profile/{profile_id}
       → No intermediate API call needed
    
    3. **Mobile App Optimization**
       - Mobile apps prefer fewer API calls (bandwidth/battery)
       - Store profile_id only (less state management)
       - Direct update without lookup
    
    4. **Real-World Scenario**
       ```
       Traditional Flow (2 API calls):
       1. GET /astrology/profile/123 → get astrology_id
       2. PATCH /astrology/{astrology_id} → update
       
       New Flow (1 API call):
       1. PATCH /astrology/profile/123 → update directly
       ```
    
    Use Cases:
    - Profile edit page: Update horoscope section
    - Admin panel: Modify user horoscope by profile
    - Mobile app: Simplified state management
    - Onboarding flow: Update horoscope after initial upload
    
    Example Request:
    PATCH /astrology/profile/123
    {
        "star": "Rohini",
        "rasi": "Taurus",
        "dosham_details": "Updated after astrologer consultation"
    }
    
    Returns: Updated astrology record
    Throws: 404 if profile has no astrology record
    """
    db_astrology = update_astrology_by_profile_id(db, profile_id, astrology)
    
    if db_astrology is None:
        raise HTTPException(
            status_code=404, 
            detail=f"No astrology details found for profile_id {profile_id}"
        )
    
    return db_astrology


@router.delete("/profile/{profile_id}", status_code=status.HTTP_200_OK)
def delete_astrology_by_profile(profile_id: int, db: Session = Depends(get_db)):
    """
    Delete astrology details by profile_id
    
    Purpose: Remove horoscope data using profile reference
    
    Why This Endpoint is Needed:
    
    1. **Privacy Compliance**
       - User requests data deletion (GDPR/privacy rights)
       - "Remove my horoscope" feature
       - Easier to implement with profile_id
    
    2. **Profile Management Workflow**
       User in profile settings:
       → "Privacy" section
       → "Remove Horoscope" button
       → DELETE /astrology/profile/{profile_id}
       → No need to know astrology_id
    
    3. **Admin Operations**
       - Admin reviewing profile reports
       - Remove inappropriate horoscope data
       - Cleanup during profile moderation
    
    4. **Re-upload Workflow**
       User uploaded wrong horoscope:
       → Delete old one: DELETE /astrology/profile/123
       → Upload new one: POST /astrology/
       → Simpler than update (avoids validation issues)
    
    5. **Bulk Operations**
       When deactivating/deleting profile:
       → Remove all related data
       → Can delete astrology by profile_id
       → Part of cascade cleanup
    
    Use Cases:
    - User privacy request: "Remove my horoscope"
    - Wrong file uploaded: Delete and re-upload
    - Profile deactivation: Cleanup related data
    - Admin moderation: Remove inappropriate content
    
    Example Request:
    DELETE /astrology/profile/123
    
    Returns: 
    {
        "message": "Deleted 1 astrology record(s) for profile_id 123"
    }
    
    Throws: 404 if profile has no astrology record
    
    Note: Returns 200 (not 204) to send deletion count in response
    """
    deleted_count = delete_astrology_by_profile_id(db, profile_id)
    
    if deleted_count is None:
        raise HTTPException(
            status_code=404, 
            detail=f"No astrology details found for profile_id {profile_id}"
        )
    
    return {
        "message": f"Deleted {deleted_count} astrology record(s) for profile_id {profile_id}",
        "profile_id": profile_id,
        "deleted_count": deleted_count
    }
