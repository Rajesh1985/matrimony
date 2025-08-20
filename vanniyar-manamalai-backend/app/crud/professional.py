from sqlalchemy.orm import Session
from models.professional import ProfessionalDetails
from schemas.professional import ProfessionalDetailsSchema

def create_professional(db: Session, professional_data: ProfessionalDetailsSchema):
    db_professional = ProfessionalDetails(**professional_data.dict())
    db.add(db_professional)
    db.commit()
    db.refresh(db_professional)
    return db_professional

def get_professional_by_profile(db: Session, profile_id: int):
    return db.query(ProfessionalDetails).filter(ProfessionalDetails.profile_id == profile_id).all()
