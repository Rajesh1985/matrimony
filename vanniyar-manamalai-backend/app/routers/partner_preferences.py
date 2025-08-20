from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.partner_preferences import PartnerPreferencesSchema
from crud.partner_preferences import create_partner_preferences, get_partner_preferences_by_profile

router = APIRouter(prefix="/partner-preferences", tags=["partner-preferences"])

@router.post("/", response_model=PartnerPreferencesSchema)
def create_new_partner_preferences(preferences: PartnerPreferencesSchema, db: Session = Depends(get_db)):
    return create_partner_preferences(db, preferences)

@router.get("/profile/{profile_id}", response_model=list[PartnerPreferencesSchema])
def read_partner_preferences_by_profile(profile_id: int, db: Session = Depends(get_db)):
    return get_partner_preferences_by_profile(db, profile_id)
