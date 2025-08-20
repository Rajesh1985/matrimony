from sqlalchemy.orm import Session
from models.profile_photo import ProfilePhoto
from schemas.profile_photo import ProfilePhotoSchema

def create_profile_photo(db: Session, photo_data: ProfilePhotoSchema):
    db_photo = ProfilePhoto(**photo_data.dict())
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo

def get_photos_by_profile(db: Session, profile_id: int):
    return db.query(ProfilePhoto).filter(ProfilePhoto.profile_id == profile_id).all()
