from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.membership import (
    MembershipCreateRequest,
    MembershipUpdateRequest,
    MembershipResponse
)
from app.crud.membership import (
    create_membership,
    get_membership,
    update_membership,
    delete_membership
)
from app.models.membership import MembershipDetails

router = APIRouter(prefix="/membership", tags=["Membership"])


@router.post("/", response_model=MembershipResponse, status_code=status.HTTP_201_CREATED)
def create_new_membership(
    membership_req: MembershipCreateRequest,
    db: Session = Depends(get_db)
):
    """
    Create or update a membership plan for a profile
    
    Purpose: Subscribe to a membership plan (Silver, Gold, or Platinum)
    
    Args:
        membership_req: MembershipCreateRequest containing:
            - profile_id (int): Profile ID
            - plan_name (str): "Silver" (3 months), "Gold" (6 months), or "Platinum" (12 months)
    
    Returns:
        MembershipResponse with membership_id, profile_id, plan_name, start_date, end_date
    
    Raises:
        400: Invalid plan_name (must be Silver, Gold, or Platinum)
        
    Example:
        POST /membership/
        {
            "profile_id": 1,
            "plan_name": "Gold"
        }
        
        Response:
        {
            "membership_id": 1,
            "profile_id": 1,
            "plan_name": "Gold",
            "start_date": "2025-12-31",
            "end_date": "2026-06-30"
        }
    """
    try:
        db_membership = create_membership(db, membership_req)
        return MembershipResponse(
            membership_id=db_membership.id,
            profile_id=db_membership.profile_id,
            plan_name=db_membership.plan_name,
            start_date=db_membership.start_date,
            end_date=db_membership.end_date
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create membership: {str(e)}"
        )


@router.get("/{profile_id}", response_model=MembershipResponse)
def get_membership_by_profile(
    profile_id: int,
    db: Session = Depends(get_db)
):
    """
    Get membership details by profile_id
    
    Purpose: Retrieve membership status and validity dates for a profile
    
    Args:
        profile_id (int): Profile ID to retrieve membership for
    
    Returns:
        MembershipResponse with membership_id, profile_id, plan_name, start_date, end_date
    
    Raises:
        404: Membership not found for profile
        
    Example:
        GET /membership/1
        
        Response:
        {
            "membership_id": 1,
            "profile_id": 1,
            "plan_name": "Gold",
            "start_date": "2025-12-31",
            "end_date": "2026-06-30"
        }
    """
    db_membership = get_membership(db, profile_id)
    
    if not db_membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Membership not found for profile {profile_id}"
        )
    
    return MembershipResponse(
        membership_id=db_membership.id,
        profile_id=db_membership.profile_id,
        plan_name=db_membership.plan_name,
        start_date=db_membership.start_date,
        end_date=db_membership.end_date
    )


@router.patch("/{profile_id}", response_model=MembershipResponse)
def update_membership_plan(
    profile_id: int,
    membership_req: MembershipUpdateRequest,
    db: Session = Depends(get_db)
):
    """
    Update or cancel a membership plan for a profile
    
    Purpose: Upgrade/downgrade membership or cancel (set to None)
    
    Args:
        profile_id (int): Profile ID to update membership for
        membership_req: MembershipUpdateRequest containing:
            - plan_name (str or null): "Silver", "Gold", "Platinum", or null to cancel
                - If null: cancels membership (plan_name, start_date, end_date all set to NULL)
                - If new plan: updates plan and recalculates end_date from today
    
    Returns:
        Updated MembershipResponse with membership_id, profile_id, plan_name, start_date, end_date
    
    Raises:
        400: Invalid plan_name (must be Silver, Gold, Platinum, or null)
        404: Membership not found for profile
        
    Example 1 - Upgrade to Platinum:
        PATCH /membership/1
        {
            "plan_name": "Platinum"
        }
        
        Response:
        {
            "membership_id": 1,
            "profile_id": 1,
            "plan_name": "Platinum",
            "start_date": "2025-12-31",
            "end_date": "2026-12-31"
        }
    
    Example 2 - Cancel membership:
        PATCH /membership/1
        {
            "plan_name": null
        }
        
        Response:
        {
            "membership_id": 1,
            "profile_id": 1,
            "plan_name": null,
            "start_date": null,
            "end_date": null
        }
    """
    try:
        db_membership = update_membership(db, profile_id, membership_req)
        
        if not db_membership:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Membership not found for profile {profile_id}"
            )
        
        return MembershipResponse(
            membership_id=db_membership.id,
            profile_id=db_membership.profile_id,
            plan_name=db_membership.plan_name,
            start_date=db_membership.start_date,
            end_date=db_membership.end_date
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update membership: {str(e)}"
        )


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_membership_plan(
    profile_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete membership record for a profile
    
    Purpose: Remove membership data completely (hard delete)
    
    Args:
        profile_id (int): Profile ID to delete membership for
    
    Returns:
        204 No Content on success
    
    Raises:
        404: Membership not found for profile
        
    Example:
        DELETE /membership/1
        
        Response: 204 No Content
    """
    success = delete_membership(db, profile_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Membership not found for profile {profile_id}"
        )
    
    return None
