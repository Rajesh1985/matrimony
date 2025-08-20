from sqlalchemy.orm import Session
from models.profile import Profile
from schemas.profile import ProfileSchema

def create_profile(db: Session, profile_data: ProfileSchema):
    db_profile = Profile(**profile_data.dict())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def get_profile(db: Session, profile_id: int):
    a = db.query(Profile).filter(Profile.id == profile_id).first()
    print(a.name)
    print(a.birth_date)
    return a

def get_profiles(db: Session):
    return db.query(Profile).all()
