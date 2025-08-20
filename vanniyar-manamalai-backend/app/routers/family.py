from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.family import FamilyDetailsSchema
from crud.family import create_family, get_family_by_profile

router = APIRouter(prefix="/family", tags=["family"])

@router.post("/", response_model=FamilyDetailsSchema)
def create_new_family(family: FamilyDetailsSchema, db: Session = Depends(get_db)):
    print("Creating new family with data:", family)
    return create_family(db, family)

@router.get("/profile/{profile_id}", response_model=list[FamilyDetailsSchema])
def read_family_by_profile(profile_id: int, db: Session = Depends(get_db)):
    return get_family_by_profile(db, profile_id)
