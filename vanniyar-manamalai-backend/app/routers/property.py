from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.property import PropertyDetailsSchema
from crud.property import create_property, get_properties_by_profile

router = APIRouter(prefix="/properties", tags=["properties"])

@router.post("/", response_model=PropertyDetailsSchema)
def create_new_property(property: PropertyDetailsSchema, db: Session = Depends(get_db)):
    return create_property(db, property)

@router.get("/profile/{profile_id}", response_model=list[PropertyDetailsSchema])
def read_properties_by_profile(profile_id: int, db: Session = Depends(get_db)):
    return get_properties_by_profile(db, profile_id)
