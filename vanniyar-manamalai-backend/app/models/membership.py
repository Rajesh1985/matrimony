from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

# ============================================================================
# VALIDATION CONSTANTS
# ============================================================================
VALID_PLAN_NAMES = {"Silver", "Gold", "Platinum"}


class MembershipDetails(Base):
    """
    MembershipDetails Model - SQLAlchemy ORM model for membership_details table
    Handles membership plans and validity periods
    """
    __tablename__ = "membership_details"
    __table_args__ = {'implicit_returning': False}

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    plan_name = Column(String(50), nullable=True)  # VARCHAR: Silver, Gold, Platinum, or NULL
    start_date = Column(Date, nullable=True)  # When membership starts
    end_date = Column(Date, nullable=True)  # When membership expires
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
