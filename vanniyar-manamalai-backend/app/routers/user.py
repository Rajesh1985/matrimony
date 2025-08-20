# Generate OTP for mobile and update
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from crud import user as crud_user
from schemas.user import UserCreate, UserOut
from typing import List

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_mobile(db, user.mobile)
    if db_user:
        raise HTTPException(status_code=400, detail="Mobile already registered")
    return crud_user.create_user(db, user)

@router.get("/{mobile}", response_model=UserOut)
def read_user(mobile: str, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_mobile(db, mobile)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# 1. Check if user exists by mobile
@router.get("/exists/{mobile}")
def is_user_by_mobile(mobile: str, db: Session = Depends(get_db)):
    return {"exists": crud_user.is_user_by_mobile(db, mobile)}

# 2. Update profile_id by mobile
@router.put("/profile_id/{mobile}")
def update_profile_id_by_mobile(mobile: str, profile_id: int, db: Session = Depends(get_db)):
    user = crud_user.update_profile_id_by_mobile(db, mobile, profile_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"success": True, "profile_id": user.profile_id}

# 3. Get profile_id by mobile
@router.get("/profile_id/{mobile}")
def get_profile_id_by_mobile(mobile: str, db: Session = Depends(get_db)):
    profile_id = crud_user.get_profile_id_by_mobile(db, mobile)
    if profile_id is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"profile_id": profile_id}

# 4. Verify OTP by mobile
@router.post("/verify_otp/{mobile}")
def verify_otp_by_mobile(mobile: str, otp: str, db: Session = Depends(get_db)):
    db_otp = crud_user.get_otp_by_mobile(db, mobile)
    if db_otp is None:
        raise HTTPException(status_code=404, detail="User not found or OTP not set")
    if db_otp == otp:
        crud_user.update_is_verified_by_mobile(db, mobile, True)
        return {"verified": True}
    return {"verified": False}

# 5. Get is_verified by mobile
@router.get("/is_verified/{mobile}")
def get_is_verified_by_mobile(mobile: str, db: Session = Depends(get_db)):
    is_verified = crud_user.get_is_verified_by_mobile(db, mobile)
    if is_verified is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"is_verified": is_verified}

@router.post("/generate_otp/{mobile}")
def generate_otp_for_mobile(mobile: str, db: Session = Depends(get_db)):
    otp_code = "1234"
    otp_created_at = datetime.now()
    user = crud_user.update_otp_by_mobile(db, mobile, otp_code, otp_created_at)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"success": True}