from sqlalchemy import Column, Integer, String, Date, Time, Boolean, ForeignKey
from database import Base

class ProfilePhoto(Base):
    __tablename__ = "profile_photos"
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"))
    photo_url = Column(String(255))
    photo_type = Column(String(20))
    upload_date = Column(Date)
    is_primary = Column(Boolean, default=False)
