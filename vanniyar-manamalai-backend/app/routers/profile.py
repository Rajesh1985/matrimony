from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.profile import ProfileSchema
from crud.profile import create_profile, get_profile, get_profiles
from models.profile import Profile

router = APIRouter(prefix="/profiles", tags=["profiles"])

@router.get("/profile_id_by_mobile/{mobile}")
def get_profile_id_by_mobile_route(mobile: str, db: Session = Depends(get_db)):
    # Directly query the profile table for mobile number
    profile = db.query(Profile).filter(Profile.mobile_number == mobile).first()
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found for mobile")
    return {"profile_id": profile.id}

@router.post("/", response_model=ProfileSchema)
def create_new_profile(profile: ProfileSchema, db: Session = Depends(get_db)):
    return create_profile(db, profile)

@router.get("/{profile_id}", response_model=ProfileSchema)
def read_profile(profile_id: int, db: Session = Depends(get_db)):
    db_profile = get_profile(db, profile_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile

@router.get("/", response_model=list[ProfileSchema])
def read_profiles(db: Session = Depends(get_db)):
    return get_profiles(db)
