from sqlalchemy.orm import Session
from . import models, schemas

def create_profile(db: Session, profile: schemas.ProfileSchema):
    db_profile = models.Profile(**profile.dict())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)

    return db_profile

def get_profile(db: Session, profile_id: int):
    return db.query(models.Profile).filter(models.Profile.id == profile_id).first()