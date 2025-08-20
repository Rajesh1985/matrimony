from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from database import Base

class EducationDetails(Base):
    __tablename__ = "education_details"
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"))
    degree = Column(String(100))
    specialization = Column(String(100))
    institution = Column(String(200))
    location = Column(String(100))
    year_of_completion = Column(Integer)
    grade_percentage = Column(DECIMAL(5,2))
