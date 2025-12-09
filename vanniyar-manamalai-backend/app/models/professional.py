from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class ProfessionalDetails(Base):
    __tablename__ = "professional_details"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    
    # Education details
    education = Column(String(100))  # Primary education (e.g., "Bachelor's in Engineering")
    education_optional = Column(String(100))  # Additional qualifications (e.g., "MBA", "CA", "PhD")
    
    # Employment details
    employment_type = Column(String(100))  # e.g., "Employed", "Self-employed", "Business", "Unemployed"
    occupation = Column(String(100))  # e.g., "Engineer", "Doctor", "Business Owner"
    company_name = Column(String(200))  # Company/Organization name
    annual_income = Column(String(100))  # Income range (e.g., "5-10 LPA", "10-15 LPA")
    work_location = Column(String(100))  # City/Country (e.g., "Chennai", "Bangalore", "USA")
