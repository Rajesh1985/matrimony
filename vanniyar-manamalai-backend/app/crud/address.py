from sqlalchemy.orm import Session
from models.address import Address
from schemas.address import AddressSchema

def create_address(db: Session, address_data: AddressSchema):
    db_address = Address(**address_data.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def get_addresses_by_profile(db: Session, profile_id: int):
    return db.query(Address).filter(Address.profile_id == profile_id).all()
