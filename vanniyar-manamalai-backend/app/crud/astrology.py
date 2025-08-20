from sqlalchemy.orm import Session
from models.astrology import AstrologyDetails
from schemas.astrology import AstrologyDetailsSchema

def create_astrology(db: Session, astrology_data: AstrologyDetailsSchema):
    db_astrology = AstrologyDetails(**astrology_data.dict())
    db.add(db_astrology)
    db.commit()
    db.refresh(db_astrology)
    return db_astrology

def get_astrology_by_profile(db: Session, profile_id: int):
    return db.query(AstrologyDetails).filter(AstrologyDetails.profile_id == profile_id).all()
