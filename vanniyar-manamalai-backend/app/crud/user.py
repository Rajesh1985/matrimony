from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate, UserUpdateMobile, PasswordUpdate
from fastapi import HTTPException
from datetime import datetime, timedelta
import secrets

def create_user(db: Session, user: UserCreate):
    """
    Create new user account
    
    Purpose: User registration for matrimony platform
    
    Security Notes:
    - Password should be hashed before storing (use passlib/bcrypt)
    - Mobile number is unique (enforced by DB)
    - profile_id is NULL initially, assigned after profile creation
    """
    try:
        db_user = User(
            country_code=user.country_code,
            name=user.name,
            mobile=user.mobile,
            email_id=user.email_id,
            password=user.password,  # TODO: Hash password in production
            gender=user.gender,
            profile_id=None,  # Assigned later after profile creation
            is_verified=False
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        db.rollback()
        if "mobile" in str(e).lower():
            raise HTTPException(status_code=400, detail="Mobile number already registered")
        raise HTTPException(status_code=400, detail="User creation failed")

def get_user_by_id(db: Session, user_id: int):
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_mobile(db: Session, mobile: str):
    """Get user by mobile number"""
    return db.query(User).filter(User.mobile == mobile).first()

def get_user_by_profile_id(db: Session, profile_id: int):
    """
    Get user by profile_id
    
    Purpose: Find user account associated with matrimony profile
    """
    return db.query(User).filter(User.profile_id == profile_id).first()

def is_user_by_mobile(db: Session, mobile: str) -> bool:
    """Check if user exists by mobile"""
    return db.query(User).filter(User.mobile == mobile).count() > 0

def update_user(db: Session, user_id: int, user_data: UserUpdate):
    """
    Update user details (excludes profile_id - immutable)
    
    Purpose: Allow users to update their account information
    
    Note: profile_id is intentionally excluded from updates
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    
    if not db_user:
        return None
    
    # Update only provided fields
    update_data = user_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def update_mobile_by_profile_id(db: Session, profile_id: int, new_mobile: str):
    """
    Update mobile number by profile_id
    
    Purpose: Allow users to change mobile number from profile context
    
    Why This is Needed:
    - User changes phone number
    - SIM card lost/stolen - need to update contact
    - Profile-centric operation (no need to know user_id)
    
    Security Considerations:
    - Should require OTP verification on both old and new numbers
    - Should check if new mobile is already registered
    
    Use Cases:
    1. User lost phone: Update to new number
    2. User changed carrier: Update mobile
    3. User wants different contact: Change number
    """
    # Check if new mobile already exists
    existing_user = db.query(User).filter(User.mobile == new_mobile).first()
    if existing_user and existing_user.profile_id != profile_id:
        raise HTTPException(status_code=400, detail="Mobile number already registered to another user")
    
    # Find user by profile_id
    db_user = db.query(User).filter(User.profile_id == profile_id).first()
    
    if not db_user:
        return None
    
    # Update mobile and reset verification
    db_user.mobile = new_mobile
    db_user.is_verified = False  # Must re-verify new number
    
    db.commit()
    db.refresh(db_user)
    return db_user

def update_password(db: Session, user_id: int, password_data: PasswordUpdate):
    """
    Update password
    
    Purpose: Allow users to change their password
    
    Security:
    - Verify old password before allowing change
    - Hash new password before storing
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    
    if not db_user:
        return None
    
    # Verify old password (TODO: Use bcrypt.verify in production)
    if db_user.password != password_data.old_password:
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    # Update password (TODO: Hash new password in production)
    db_user.password = password_data.new_password
    
    db.commit()
    db.refresh(db_user)
    return db_user

def update_profile_id_by_mobile(db: Session, mobile: str, profile_id: int):
    """
    Assign profile_id to user after profile creation
    
    Purpose: Link user account to matrimony profile
    
    Workflow:
    1. User registers (creates user account)
    2. User creates profile (creates profile record)
    3. System links them using this method
    """
    db_user = db.query(User).filter(User.mobile == mobile).first()
    
    if not db_user:
        return None
    
    db_user.profile_id = profile_id
    
    db.commit()
    db.refresh(db_user)
    return db_user

def get_profile_id_by_mobile(db: Session, mobile: str):
    """Get profile_id by mobile number"""
    db_user = db.query(User).filter(User.mobile == mobile).first()
    return db_user.profile_id if db_user else None

# ==================== OTP OPERATIONS ====================

def generate_otp(db: Session, mobile: str):
    """
    Generate and store OTP for mobile verification
    
    Purpose: Send OTP for mobile number verification
    
    Production Implementation:
    - Generate random 6-digit OTP
    - Store with expiry time (5-10 minutes)
    - Send via SMS gateway (Twilio/AWS SNS)
    - Rate limit to prevent abuse
    """
    db_user = db.query(User).filter(User.mobile == mobile).first()
    
    if not db_user:
        return None
    
    # Generate OTP (production: use secrets.randbelow or similar)
    otp_code = str(secrets.randbelow(900000) + 100000)  # 6-digit random number
    otp_created_at = datetime.now()
    
    db_user.otp_code = otp_code
    db_user.otp_created_at = otp_created_at
    
    db.commit()
    db.refresh(db_user)
    
    # TODO: Send OTP via SMS gateway
    # send_sms(mobile, f"Your OTP is: {otp_code}")
    
    return db_user

def verify_otp(db: Session, mobile: str, otp_code: str):
    """
    Verify OTP and mark user as verified
    
    Purpose: Confirm mobile number ownership
    
    Security:
    - Check OTP expiry (5-10 minutes)
    - Limit verification attempts (3-5 tries)
    - Clear OTP after successful verification
    """
    db_user = db.query(User).filter(User.mobile == mobile).first()
    
    if not db_user:
        return None
    
    # Check if OTP expired (10 minutes)
    if db_user.otp_created_at:
        expiry_time = db_user.otp_created_at + timedelta(minutes=10)
        if datetime.now() > expiry_time:
            raise HTTPException(status_code=400, detail="OTP expired. Please request a new one.")
    
    # Verify OTP
    if db_user.otp_code != otp_code:
        return False
    
    # Mark as verified and clear OTP
    db_user.is_verified = True
    db_user.otp_code = None
    db_user.otp_created_at = None
    
    db.commit()
    db.refresh(db_user)
    
    return True

def update_is_verified_by_mobile(db: Session, mobile: str, is_verified: bool):
    """Update verification status"""
    db_user = db.query(User).filter(User.mobile == mobile).first()
    
    if not db_user:
        return None
    
    db_user.is_verified = is_verified
    
    db.commit()
    db.refresh(db_user)
    return db_user

def get_is_verified_by_mobile(db: Session, mobile: str):
    """Get verification status"""
    db_user = db.query(User).filter(User.mobile == mobile).first()
    return db_user.is_verified if db_user else None

# ==================== AUTHENTICATION ====================

def authenticate_user(db: Session, mobile: str, password: str):
    """
    Authenticate user login
    
    Purpose: Verify credentials and return user
    
    Security:
    - Should use bcrypt.verify for password checking
    - Should implement rate limiting (prevent brute force)
    - Should log failed attempts
    """
    db_user = db.query(User).filter(User.mobile == mobile).first()
    
    if not db_user:
        return None
    
    # Verify password (TODO: Use bcrypt.verify in production)
    if db_user.password != password:
        return None
    
    return db_user

# ==================== ADMIN/SEARCH OPERATIONS ====================

def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    """Get all users (admin operation)"""
    return db.query(User).offset(skip).limit(limit).all()

def get_users_by_gender(db: Session, gender: str, skip: int = 0, limit: int = 100):
    """
    Get users by gender
    
    Purpose: Admin analytics, gender-based statistics
    """
    return (
        db.query(User)
        .filter(User.gender == gender)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_verified_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Get verified users only
    
    Purpose: Filter genuine users (verified mobile)
    """
    return (
        db.query(User)
        .filter(User.is_verified == True)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_users_with_profile(db: Session, skip: int = 0, limit: int = 100):
    """
    Get users who have created profiles
    
    Purpose: Find users who completed profile creation
    """
    return (
        db.query(User)
        .filter(User.profile_id.isnot(None))
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_users_without_profile(db: Session, skip: int = 0, limit: int = 100):
    """
    Get users who haven't created profiles
    
    Purpose: Find incomplete registrations
    Use Case: Send reminder emails/notifications
    """
    return (
        db.query(User)
        .filter(User.profile_id.is_(None))
        .offset(skip)
        .limit(limit)
        .all()
    )

def delete_user(db: Session, user_id: int):
    """
    Delete user account
    
    Purpose: User requests account deletion (GDPR compliance)
    
    Note: Should also delete associated profile and related data
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    
    if not db_user:
        return None
    
    db.delete(db_user)
    db.commit()
    return db_user
