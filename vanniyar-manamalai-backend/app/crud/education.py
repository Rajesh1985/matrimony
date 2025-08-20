from sqlalchemy.orm import Session
from models.education import EducationDetails
from schemas.education import EducationDetailsSchema

def create_education(db: Session, education_data: EducationDetailsSchema):
    db_education = EducationDetails(**education_data.dict())
    db.add(db_education)
    db.commit()
    db.refresh(db_education)
    return db_education

def get_education_by_profile(db: Session, profile_id: int):
    return db.query(EducationDetails).filter(EducationDetails.profile_id == profile_id).all()
