from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.education import EducationDetailsSchema
from crud.education import create_education, get_education_by_profile

router = APIRouter(prefix="/education", tags=["education"])

@router.post("/", response_model=EducationDetailsSchema)
def create_new_education(education: EducationDetailsSchema, db: Session = Depends(get_db)):
    return create_education(db, education)

@router.get("/profile/{profile_id}", response_model=list[EducationDetailsSchema])
def read_education_by_profile(profile_id: int, db: Session = Depends(get_db)):
    return get_education_by_profile(db, profile_id)
