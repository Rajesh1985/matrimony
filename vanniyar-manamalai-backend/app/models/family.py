from sqlalchemy import Column, Integer, String, ForeignKey, Text, Enum, CheckConstraint
from app.database import Base
import enum

class FamilyStatusEnum(str, enum.Enum):
    """Economic status of family"""
    Middle_Class = "Middle_Class"
    Upper_Middle_Class = "Upper_Middle_Class"
    Rich_Elite = "Rich_Elite"

class FamilyTypeEnum(str, enum.Enum):
    """Family structure type"""
    nuclear = "nuclear"
    joint = "joint"
    extended = "extended"

class FamilyDetails(Base):
    __tablename__ = "family_details"
    __table_args__ = (
        CheckConstraint(
            "family_type IN ('nuclear', 'joint', 'extended')",
            name="check_family_type"
        ),
    )
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    
    # Parent details
    father_name = Column(String(100))
    father_occupation = Column(String(100))
    mother_name = Column(String(100))
    mother_occupation = Column(String(100))
    
    # Sibling details (granular tracking)
    brothers = Column(Integer, default=0)
    sisters = Column(Integer, default=0)
    Married_brothers = Column(Integer, default=0)  # Note: Capital 'M' to match DB
    Married_sisters = Column(Integer, default=0)   # Note: Capital 'M' to match DB
    
    # Family structure
    family_type = Column(String(20), default='nuclear')
    family_status = Column(Enum(FamilyStatusEnum))
    Family_description = Column(Text)  # Note: Capital 'F' to match DB
