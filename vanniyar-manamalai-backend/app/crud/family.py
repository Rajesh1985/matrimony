from sqlalchemy.orm import Session
from models.family import FamilyDetails
from schemas.family import FamilyDetailsSchema

def create_family(db: Session, family_data: FamilyDetailsSchema):
    print("Creating new family with data:", family_data)
    db_family = FamilyDetails(**family_data.dict())
    db.add(db_family)
    db.commit()
    db.refresh(db_family)
    return db_family

def get_family_by_profile(db: Session, profile_id: int):
    return db.query(FamilyDetails).filter(FamilyDetails.profile_id == profile_id).all()
