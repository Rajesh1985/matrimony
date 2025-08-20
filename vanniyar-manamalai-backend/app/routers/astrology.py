from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.astrology import AstrologyDetailsSchema
from crud.astrology import create_astrology, get_astrology_by_profile

router = APIRouter(prefix="/astrology", tags=["astrology"])

@router.post("/", response_model=AstrologyDetailsSchema)
def create_new_astrology(astrology: AstrologyDetailsSchema, db: Session = Depends(get_db)):
    return create_astrology(db, astrology)

@router.get("/profile/{profile_id}", response_model=list[AstrologyDetailsSchema])
def read_astrology_by_profile(profile_id: int, db: Session = Depends(get_db)):
    return get_astrology_by_profile(db, profile_id)
