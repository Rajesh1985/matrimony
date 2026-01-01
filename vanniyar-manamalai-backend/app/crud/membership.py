from sqlalchemy.orm import Session
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from typing import Optional
from app.models.membership import MembershipDetails, VALID_PLAN_NAMES
from app.schemas.membership import MembershipCreateRequest, MembershipUpdateRequest


def create_membership(db: Session, membership_data: MembershipCreateRequest) -> MembershipDetails:
    """
    Create a new membership record
    
    Args:
        db: Database session
        membership_data: MembershipCreateRequest containing profile_id and plan_name
    
    Returns:
        Created MembershipDetails object
        
    Raises:
        ValueError: If plan_name is invalid
        
    Example:
        membership = create_membership(db, MembershipCreateRequest(profile_id=1, plan_name="Gold"))
    """
    # Validate plan_name
    if membership_data.plan_name not in VALID_PLAN_NAMES:
        raise ValueError(f"Invalid plan name: {membership_data.plan_name}")
    
    # Calculate start and end dates
    today = date.today()
    start_date = today
    
    # Calculate end_date based on plan_name
    if membership_data.plan_name == "Silver":
        end_date = today + relativedelta(months=3)
    elif membership_data.plan_name == "Gold":
        end_date = today + relativedelta(months=6)
    elif membership_data.plan_name == "Platinum":
        end_date = today + relativedelta(months=12)
    else:
        raise ValueError(f"Invalid plan name: {membership_data.plan_name}")
    
    # Check if membership already exists for this profile
    existing = db.query(MembershipDetails).filter(
        MembershipDetails.profile_id == membership_data.profile_id
    ).first()
    
    if existing:
        # Update existing membership
        existing.plan_name = membership_data.plan_name
        existing.start_date = start_date
        existing.end_date = end_date
        existing.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # Create new membership
        db_membership = MembershipDetails(
            profile_id=membership_data.profile_id,
            plan_name=membership_data.plan_name,
            start_date=start_date,
            end_date=end_date
        )
        db.add(db_membership)
        db.commit()
        db.refresh(db_membership)
        return db_membership


def get_membership(db: Session, profile_id: int) -> Optional[MembershipDetails]:
    """
    Get membership by profile_id
    
    Args:
        db: Database session
        profile_id: The profile ID to retrieve membership for
    
    Returns:
        MembershipDetails object or None if not found
        
    Example:
        membership = get_membership(db, profile_id=1)
    """
    return db.query(MembershipDetails).filter(
        MembershipDetails.profile_id == profile_id
    ).first()


def update_membership(db: Session, profile_id: int, membership_data: MembershipUpdateRequest) -> Optional[MembershipDetails]:
    """
    Update membership by profile_id
    
    Args:
        db: Database session
        profile_id: The profile ID to update membership for
        membership_data: MembershipUpdateRequest containing new plan_name or None to cancel
    
    Returns:
        Updated MembershipDetails object or None if not found
        
    Raises:
        ValueError: If plan_name is invalid
        
    Example:
        membership = update_membership(db, profile_id=1, MembershipUpdateRequest(plan_name="Platinum"))
    """
    db_membership = db.query(MembershipDetails).filter(
        MembershipDetails.profile_id == profile_id
    ).first()
    
    if not db_membership:
        return None
    
    # If plan_name is None, cancel membership
    if membership_data.plan_name is None:
        db_membership.plan_name = None
        db_membership.start_date = None
        db_membership.end_date = None
        db_membership.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_membership)
        return db_membership
    
    # Validate plan_name
    if membership_data.plan_name not in VALID_PLAN_NAMES:
        raise ValueError(f"Invalid plan name: {membership_data.plan_name}")
    
    # Keep existing start_date, recalculate end_date from today
    today = date.today()
    
    # Calculate new end_date based on plan_name
    if membership_data.plan_name == "Silver":
        new_end_date = today + relativedelta(months=3)
    elif membership_data.plan_name == "Gold":
        new_end_date = today + relativedelta(months=6)
    elif membership_data.plan_name == "Platinum":
        new_end_date = today + relativedelta(months=12)
    else:
        raise ValueError(f"Invalid plan name: {membership_data.plan_name}")
    
    # Update membership
    db_membership.plan_name = membership_data.plan_name
    db_membership.end_date = new_end_date
    db_membership.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_membership)
    return db_membership


def delete_membership(db: Session, profile_id: int) -> bool:
    """
    Delete membership by profile_id
    
    Args:
        db: Database session
        profile_id: The profile ID to delete membership for
    
    Returns:
        True if deleted, False if not found
        
    Example:
        success = delete_membership(db, profile_id=1)
    """
    db_membership = db.query(MembershipDetails).filter(
        MembershipDetails.profile_id == profile_id
    ).first()
    
    if not db_membership:
        return False
    
    db.delete(db_membership)
    db.commit()
    return True
