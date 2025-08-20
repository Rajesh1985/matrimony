from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.professional import ProfessionalDetailsSchema
from crud.professional import create_professional, get_professional_by_profile

router = APIRouter(prefix="/professional", tags=["professional"])

@router.post("/", response_model=ProfessionalDetailsSchema)
def create_new_professional(professional: ProfessionalDetailsSchema, db: Session = Depends(get_db)):
    return create_professional(db, professional)

@router.get("/profile/{profile_id}", response_model=list[ProfessionalDetailsSchema])
def read_professional_by_profile(profile_id: int, db: Session = Depends(get_db)):
    return get_professional_by_profile(db, profile_id)
