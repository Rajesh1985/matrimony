from sqlalchemy.orm import Session
from models.partner_preferences import PartnerPreferences
from schemas.partner_preferences import PartnerPreferencesSchema

def create_partner_preferences(db: Session, preferences_data: PartnerPreferencesSchema):
    db_preferences = PartnerPreferences(**preferences_data.dict())
    db.add(db_preferences)
    db.commit()
    db.refresh(db_preferences)
    return db_preferences

def get_partner_preferences_by_profile(db: Session, profile_id: int):
    return db.query(PartnerPreferences).filter(PartnerPreferences.profile_id == profile_id).all()
