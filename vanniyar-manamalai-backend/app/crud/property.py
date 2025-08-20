from sqlalchemy.orm import Session
from models.property import PropertyDetails
from schemas.property import PropertyDetailsSchema

def create_property(db: Session, property_data: PropertyDetailsSchema):
    db_property = PropertyDetails(**property_data.dict())
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property

def get_properties_by_profile(db: Session, profile_id: int):
    return db.query(PropertyDetails).filter(PropertyDetails.profile_id == profile_id).all()
