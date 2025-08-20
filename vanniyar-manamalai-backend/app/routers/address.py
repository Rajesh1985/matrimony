from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.address import AddressSchema
from crud.address import create_address, get_addresses_by_profile

router = APIRouter(prefix="/addresses", tags=["addresses"])

@router.post("/", response_model=AddressSchema)
def create_new_address(address: AddressSchema, db: Session = Depends(get_db)):
    return create_address(db, address)

@router.get("/profile/{profile_id}", response_model=list[AddressSchema])
def read_addresses_by_profile(profile_id: int, db: Session = Depends(get_db)):
    return get_addresses_by_profile(db, profile_id)
