from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate

def create_user(db: Session, user: UserCreate):
    db_user = User(
        country_code=user.country_code,
        mobile=user.mobile,
        password=user.password,
        name=user.name,
        email_id=user.email_id,
        gender=user.gender,
        profile_id=user.profile_id if hasattr(user, 'profile_id') and user.profile_id is not None else 0  # default to 0
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_mobile(db: Session, mobile: str):
    user = db.query(User).filter(User.mobile == mobile).first()
    if user:
        # Ensure profile_id is never None
        user.profile_id = user.profile_id if user.profile_id is not None else 0
    return user

def is_user_by_mobile(db: Session, mobile: str) -> bool:
    return db.query(User).filter(User.mobile == mobile).count() > 0

# 1. Update profile_id by mobile
def update_profile_id_by_mobile(db: Session, mobile: str, profile_id: int):
    user = db.query(User).filter(User.mobile == mobile).first()
    if user:
        user.profile_id = profile_id
        db.commit()
        db.refresh(user)
    return user

# 2. Get profile_id by mobile
def get_profile_id_by_mobile(db: Session, mobile: str):
    user = db.query(User).filter(User.mobile == mobile).first()
    return user.profile_id if user else None

# 3. Update otp and otp time by mobile
def update_otp_by_mobile(db: Session, mobile: str, otp_code: str, otp_created_at):
    user = db.query(User).filter(User.mobile == mobile).first()
    if user:
        user.otp_code = otp_code
        user.otp_created_at = otp_created_at
        db.commit()
        db.refresh(user)
    return user

# 4. Get otp by mobile
def get_otp_by_mobile(db: Session, mobile: str):
    user = db.query(User).filter(User.mobile == mobile).first()
    return user.otp_code if user else None

# 5. Update is_verified by mobile
def update_is_verified_by_mobile(db: Session, mobile: str, is_verified: bool):
    user = db.query(User).filter(User.mobile == mobile).first()
    if user:
        user.is_verified = is_verified
        db.commit()
        db.refresh(user)
    return user

# 6. Get is_verified by mobile
def get_is_verified_by_mobile(db: Session, mobile: str):
    user = db.query(User).filter(User.mobile == mobile).first()
    return user.is_verified if user else None

def get_all_users(db: Session):
    return db.query(User).all()
