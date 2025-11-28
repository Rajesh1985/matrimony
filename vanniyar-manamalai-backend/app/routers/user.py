from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import user as crud_user
from app.schemas.user import (
    UserCreate, 
    UserUpdate, 
    UserUpdateMobile,
    UserResponse, 
    UserLogin,
    OTPRequest,
    OTPVerify,
    PasswordUpdate,
    UserSearchFilters
)

router = APIRouter(prefix="/users", tags=["users"])

# ==================== USER REGISTRATION & RETRIEVAL ====================

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register new user
    
    Purpose: User registration for matrimony platform
    
    Workflow:
    1. User provides: mobile, name, email, password, gender
    2. System creates user account (profile_id is NULL)
    3. User receives OTP for verification
    4. After verification, user creates matrimony profile
    5. profile_id is assigned to link account and profile
    
    Security:
    - Mobile must be unique
    - Password should be hashed (implement in production)
    - Send OTP for verification
    """
    db_user = crud_user.get_user_by_mobile(db, user.mobile)
    if db_user:
        raise HTTPException(status_code=400, detail="Mobile already registered")
    
    return crud_user.create_user(db, user)

@router.get("/mobile/{mobile}", response_model=UserResponse)
def read_user_by_mobile(mobile: str, db: Session = Depends(get_db)):
    """
    Get user by mobile number
    
    Purpose: Lookup user account by mobile
    """
    db_user = crud_user.get_user_by_mobile(db, mobile)
    
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return db_user

@router.get("/profile/{profile_id}", response_model=UserResponse)
def read_user_by_profile_id(profile_id: int, db: Session = Depends(get_db)):
    """
    Get user by profile_id
    
    Purpose: Find user account from matrimony profile
    Use Case: Display user contact info on profile page
    """
    db_user = crud_user.get_user_by_profile_id(db, profile_id)
    
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found for this profile")
    
    return db_user

@router.get("/{user_id}", response_model=UserResponse)
def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID"""
    db_user = crud_user.get_user_by_id(db, user_id)
    
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return db_user

# ==================== USER UPDATES ====================

@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    """
    Update user details (excludes profile_id - immutable)
    
    Purpose: Allow users to update their account information
    
    Updatable Fields:
    - name: Change display name
    - email_id: Update email address
    - gender: Update gender (if needed)
    
    Non-Updatable:
    - profile_id: Immutable after assignment
    - mobile: Use separate endpoint with OTP verification
    - password: Use separate password update endpoint
    
    Use Cases:
    - User corrects name spelling
    - User updates email address
    - User profile information changes
    
    Example Request:
    PATCH /users/123
    {
        "name": "Updated Name",
        "email_id": "newemail@example.com"
    }
    """
    db_user = crud_user.update_user(db, user_id, user)
    
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return db_user

@router.patch("/mobile/profile/{profile_id}", response_model=UserResponse)
def update_mobile_by_profile(
    profile_id: int,
    mobile_data: UserUpdateMobile,
    db: Session = Depends(get_db)
):
    """
    Update mobile number by profile_id
    
    Purpose: Allow users to change mobile number from profile context
    
    Why This Endpoint is Needed:
    
    1. **Profile-Centric Operation**
       - Frontend has profile_id from session
       - No need to fetch user_id first
       - Simpler API workflow
    
    2. **Real-World Scenarios**
       - Lost phone: Need to update contact number
       - Changed carrier: New mobile number
       - Security: Stolen SIM card
       - Preference: Want different contact
    
    3. **Security Considerations**
       - New mobile must not be already registered
       - Should send OTP to both old and new numbers
       - User must verify both numbers
       - Resets is_verified to False (must re-verify)
    
    Workflow:
    1. User requests mobile change from profile settings
    2. System sends OTP to old mobile (confirm it's really user)
    3. User verifies old mobile OTP
    4. System sends OTP to new mobile
    5. User verifies new mobile OTP
    6. System updates mobile number
    7. is_verified reset to False (must verify new number)
    
    Use Cases:
    - User: "I lost my phone, update to new number"
    - User: "Changed to different mobile, update contact"
    - Admin: "User requested mobile change via support"
    
    Example Request:
    PATCH /users/mobile/profile/123
    {
        "new_mobile": "9876543210",
        "otp_code": "123456"  # Optional: for verification
    }
    
    Returns: Updated user record
    Throws: 
    - 404 if profile not found
    - 400 if new mobile already registered
    """
    db_user = crud_user.update_mobile_by_profile_id(db, profile_id, mobile_data.new_mobile)
    
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail=f"No user found for profile_id {profile_id}"
        )
    
    return db_user

@router.patch("/{user_id}/password")
def update_password(
    user_id: int,
    password_data: PasswordUpdate,
    db: Session = Depends(get_db)
):
    """
    Update user password
    
    Purpose: Allow users to change their password
    
    Security:
    - Requires old password verification
    - New password must meet minimum requirements (6 chars)
    - Should hash password before storing (implement in production)
    
    Use Cases:
    - User: "I want to change my password"
    - Security: "Suspected account compromise"
    - Policy: "Regular password rotation"
    
    Example Request:
    PATCH /users/123/password
    {
        "old_password": "oldpass123",
        "new_password": "newpass456"
    }
    """
    db_user = crud_user.update_password(db, user_id, password_data)
    
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"success": True, "message": "Password updated successfully"}

# ==================== PROFILE LINKING ====================

@router.put("/profile_id/{mobile}")
def update_profile_id_by_mobile(mobile: str, profile_id: int, db: Session = Depends(get_db)):
    """
    Assign profile_id to user (internal operation)
    
    Purpose: Link user account to matrimony profile after profile creation
    
    Workflow:
    1. User registers (creates user account)
    2. User creates matrimony profile (separate API call)
    3. Backend calls this endpoint to link user and profile
    
    This is typically called internally, not by frontend directly.
    """
    user = crud_user.update_profile_id_by_mobile(db, mobile, profile_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"success": True, "profile_id": user.profile_id}

@router.get("/profile_id/{mobile}")
def get_profile_id_by_mobile(mobile: str, db: Session = Depends(get_db)):
    """
    Get profile_id by mobile number
    
    Purpose: Find matrimony profile associated with mobile
    Use Case: Quick profile lookup from mobile number
    """
    profile_id = crud_user.get_profile_id_by_mobile(db, mobile)
    
    if profile_id is None:
        raise HTTPException(status_code=404, detail="User not found or no profile linked")
    
    return {"profile_id": profile_id}

# ==================== OTP & VERIFICATION ====================

@router.post("/generate_otp")
def generate_otp_for_mobile(request: OTPRequest, db: Session = Depends(get_db)):
    """
    Generate and send OTP
    
    Purpose: Mobile number verification
    
    Workflow:
    1. User requests OTP
    2. System generates 6-digit random OTP
    3. System stores OTP with timestamp
    4. System sends OTP via SMS (implement in production)
    5. OTP expires in 10 minutes
    
    Security:
    - Rate limit: 3 OTPs per hour per mobile
    - Auto-expire after 10 minutes
    - Clear OTP after successful verification
    
    Production Implementation:
    - Use SMS gateway (Twilio/AWS SNS/MSG91)
    - Implement rate limiting
    - Log OTP requests for audit
    """
    user = crud_user.generate_otp(db, request.mobile)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # TODO: Send OTP via SMS in production
    return {
        "success": True,
        "message": "OTP sent successfully",
        "otp": user.otp_code  # Remove this in production (for testing only)
    }

@router.post("/verify_otp")
def verify_otp_by_mobile(request: OTPVerify, db: Session = Depends(get_db)):
    """
    Verify OTP
    
    Purpose: Confirm mobile number ownership
    
    Workflow:
    1. User receives OTP on mobile
    2. User enters OTP in app
    3. System verifies OTP
    4. If correct: Mark user as verified, clear OTP
    5. If wrong: Return error (limit attempts)
    
    Security:
    - Check OTP expiry (10 minutes)
    - Limit verification attempts (3-5 tries)
    - Clear OTP after successful verification
    - Auto-block after max failed attempts
    """
    result = crud_user.verify_otp(db, request.mobile, request.otp_code)
    
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if result:
        return {"verified": True, "message": "Mobile number verified successfully"}
    else:
        return {"verified": False, "message": "Invalid OTP"}

@router.get("/is_verified/{mobile}")
def get_is_verified_by_mobile(mobile: str, db: Session = Depends(get_db)):
    """
    Get verification status
    
    Purpose: Check if user has verified mobile
    """
    is_verified = crud_user.get_is_verified_by_mobile(db, mobile)
    
    if is_verified is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"is_verified": is_verified}

# ==================== AUTHENTICATION ====================

@router.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    User login
    
    Purpose: Authenticate user and return profile_id
    
    Workflow:
    1. User provides mobile + password
    2. System verifies credentials
    3. System checks if user is verified
    4. Return profile_id for session
    
    Security:
    - Should implement JWT tokens in production
    - Should rate limit failed attempts
    - Should log login attempts
    - Should enforce verified status
    
    Production Implementation:
    - Generate JWT token
    - Set session/cookie
    - Return token + user details
    """
    db_user = crud_user.authenticate_user(db, credentials.mobile, credentials.password)
    
    if db_user is None:
        raise HTTPException(status_code=401, detail="Invalid mobile or password")
    
    if not db_user.is_verified:
        raise HTTPException(status_code=403, detail="Please verify your mobile number first")
    
    return {
        "success": True,
        "user_id": db_user.id,
        "profile_id": db_user.profile_id,
        "name": db_user.name,
        "is_verified": db_user.is_verified
    }

@router.post("/validate")
def validate_user(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Validate user credentials (deprecated - use /login)
    
    Purpose: Legacy endpoint for credential validation
    Note: Use /login endpoint instead
    """
    db_user = crud_user.authenticate_user(db, credentials.mobile, credentials.password)
    
    if db_user is None:
        return {"valid": False}
    
    return {"valid": True, "profile_id": db_user.profile_id}

# ==================== UTILITY ENDPOINTS ====================

@router.get("/exists/{mobile}")
def is_user_by_mobile(mobile: str, db: Session = Depends(get_db)):
    """
    Check if user exists by mobile
    
    Purpose: Pre-registration check
    Use Case: "Mobile already registered" validation
    """
    return {"exists": crud_user.is_user_by_mobile(db, mobile)}

# ==================== ADMIN/SEARCH ENDPOINTS ====================

@router.get("/admin/all", response_model=list[UserResponse])
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all users (admin operation)
    
    Purpose: Admin dashboard - user list
    Security: Should require admin authentication
    """
    return crud_user.get_all_users(db, skip, limit)

@router.get("/admin/gender/{gender}", response_model=list[UserResponse])
def get_users_by_gender(gender: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get users by gender
    
    Purpose: Admin analytics - gender distribution
    """
    return crud_user.get_users_by_gender(db, gender, skip, limit)

@router.get("/admin/verified", response_model=list[UserResponse])
def get_verified_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get verified users only
    
    Purpose: Filter genuine users (verified mobile)
    """
    return crud_user.get_verified_users(db, skip, limit)

@router.get("/admin/with-profile", response_model=list[UserResponse])
def get_users_with_profile(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get users who have created profiles
    
    Purpose: Find users who completed registration
    """
    return crud_user.get_users_with_profile(db, skip, limit)

@router.get("/admin/without-profile", response_model=list[UserResponse])
def get_users_without_profile(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get users who haven't created profiles
    
    Purpose: Find incomplete registrations
    Use Case: Send reminder to complete profile
    """
    return crud_user.get_users_without_profile(db, skip, limit)

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete user account
    
    Purpose: Account deletion (GDPR compliance)
    
    Security:
    - Should require authentication
    - Should confirm with user (email/SMS)
    - Should delete associated data (profile, photos, etc.)
    
    Use Cases:
    - User requests account deletion
    - Admin removes spam/fake accounts
    - Compliance with data protection laws
    """
    db_user = crud_user.delete_user(db, user_id)
    
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"success": True, "message": "User account deleted"}
