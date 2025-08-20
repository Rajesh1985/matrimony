from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.profile_photo import ProfilePhotoSchema
from crud.profile_photo import create_profile_photo, get_photos_by_profile

router = APIRouter(prefix="/profile-photos", tags=["profile-photos"])

@router.post("/", response_model=ProfilePhotoSchema)
def create_new_profile_photo(photo: ProfilePhotoSchema, db: Session = Depends(get_db)):
    return create_profile_photo(db, photo)

@router.get("/profile/{profile_id}", response_model=list[ProfilePhotoSchema])
def read_photos_by_profile(profile_id: int, db: Session = Depends(get_db)):
    return get_photos_by_profile(db, profile_id)
