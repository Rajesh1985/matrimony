from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from database import Base

class ProfessionalDetails(Base):
    __tablename__ = "professional_details"
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"))
    designation = Column(String(100))
    company_name = Column(String(200))
    industry = Column(String(100))
    experience_years = Column(DECIMAL(4,1))
    monthly_income = Column(DECIMAL(12,2))
    annual_income = Column(DECIMAL(12,2))
    work_location = Column(String(100))
