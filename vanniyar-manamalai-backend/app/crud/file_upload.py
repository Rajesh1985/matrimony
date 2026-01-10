# app/crud/file_upload.py
"""
CRUD operations for file uploads with profile photo integration
- Create file records
- Find duplicate files
- Update file metadata
- Assign photo slots in family_details
- Delete files and cleanup
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.file import File, ProcessingStatusEnum, FileKindEnum
from app.models.family import FamilyDetails
from app.models.profile import Profile
from datetime import datetime
from typing import Optional, Tuple


# ==================== FILE RECORD MANAGEMENT ====================

def create_file_record(
    db: Session,
    file_id: str,
    original_name: str,
    mime_type: str,
    size_bytes: int,
    checksum: str,
    storage_path: str,
    thumbnail_path: Optional[str] = None,
    processing_status: str = ProcessingStatusEnum.ready,
    width: Optional[int] = None,
    height: Optional[int] = None
) -> File:
    """
    Create a new file record in database
    
    Args:
        db: Database session
        file_id: Unique file identifier
        original_name: Original filename
        mime_type: MIME type
        size_bytes: File size in bytes
        checksum: SHA256 checksum
        storage_path: Path to stored file
        thumbnail_path: Path to thumbnail (if image)
        processing_status: Processing status enum
        width: Image width (if image)
        height: Image height (if image)
    
    Returns:
        Created File object
    """
    db_file = File(
        id=file_id,
        original_name=original_name,
        file_kind=FileKindEnum.image if mime_type.startswith('image/') else FileKindEnum.pdf,
        mime_type=mime_type,
        size_bytes=size_bytes,
        checksum=checksum,
        storage_path=storage_path,
        thumbnail_path=thumbnail_path,
        processing_status=processing_status,
        width=width,
        height=height,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


def get_file_by_id(db: Session, file_id: str) -> Optional[File]:
    """
    Get file by ID
    
    Args:
        db: Database session
        file_id: File ID
    
    Returns:
        File object or None
    """
    return db.query(File).filter(File.id == file_id).first()


def find_duplicate_by_checksum(db: Session, checksum: str) -> Optional[File]:
    """
    Find existing file by checksum (duplicate detection)
    
    Args:
        db: Database session
        checksum: SHA256 checksum
    
    Returns:
        Existing File object if duplicate found, None otherwise
    """
    print(f"[find_duplicate_by_checksum] Checking for duplicate with checksum: {checksum}")
    return db.query(File).filter(
        and_(
            File.checksum == checksum,
            File.processing_status == ProcessingStatusEnum.ready
        )
    ).first()


def update_file_record(
    db: Session,
    file_id: str,
    **kwargs
) -> Optional[File]:
    """
    Update file record
    
    Args:
        db: Database session
        file_id: File ID
        **kwargs: Fields to update
    
    Returns:
        Updated File object
    """
    db_file = get_file_by_id(db, file_id)
    if not db_file:
        return None
    
    for key, value in kwargs.items():
        if hasattr(db_file, key):
            setattr(db_file, key, value)
    
    db_file.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_file)
    return db_file


def delete_file_record(db: Session, file_id: str) -> bool:
    """
    Delete file record from database
    
    Args:
        db: Database session
        file_id: File ID
    
    Returns:
        True if successful, False if not found
    """
    db_file = get_file_by_id(db, file_id)
    if not db_file:
        return False
    
    db.delete(db_file)
    db.commit()
    return True


# ==================== PHOTO SLOT ASSIGNMENT ====================

def get_profile_with_family(db: Session, profile_id: int) -> Optional[Tuple[Profile, FamilyDetails]]:
    """
    Get profile and family details
    
    Args:
        db: Database session
        profile_id: Profile ID
    
    Returns:
        Tuple[Profile, FamilyDetails] or None
    """
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        return None
    
    family = db.query(FamilyDetails).filter(FamilyDetails.profile_id == profile_id).first()
    return profile, family


def find_available_photo_slot(db: Session, profile_id: int) -> Tuple[int, Optional[str]]:
    """
    Find available photo slot in family_details
    
    Returns: Tuple[slot_number, error_code]
    - Slot 1: photo_file_id_1
    - Slot 2: photo_file_id_2
    
    Args:
        db: Database session
        profile_id: Profile ID
    
    Returns:
        Tuple[slot_number, error_code]
        - (1, None) if slot 1 available
        - (2, None) if slot 1 taken, slot 2 available
        - (None, "NO_FREE_SLOT") if both slots taken
    """
    family = db.query(FamilyDetails).filter(FamilyDetails.profile_id == profile_id).first()
    
    if not family:
        # Family record doesn't exist, can use slot 1
        return 1, None
    
    # Check if photo_file_id_1 exists (need to add columns first)
    if not hasattr(family, 'photo_file_id_1') or family.photo_file_id_1 is None:
        return 1, None
    
    # Check if photo_file_id_2 exists
    if not hasattr(family, 'photo_file_id_2') or family.photo_file_id_2 is None:
        return 2, None
    
    # Both slots taken
    return None, "NO_FREE_SLOT"


def assign_photo_to_slot(
    db: Session,
    profile_id: int,
    file_id: str,
    slot_number: int
) -> bool:
    """
    Assign file to photo slot in family_details
    
    Args:
        db: Database session
        profile_id: Profile ID
        file_id: File ID to assign
        slot_number: Slot number (1 or 2)
    
    Returns:
        True if successful, False if error
    """
    family = db.query(FamilyDetails).filter(FamilyDetails.profile_id == profile_id).first()
    
    if not family:
        # Create family record if doesn't exist
        family = FamilyDetails(profile_id=profile_id)
        db.add(family)
        db.flush()
    
    # Assign to appropriate slot
    if slot_number == 1:
        family.photo_file_id_1 = file_id
    elif slot_number == 2:
        family.photo_file_id_2 = file_id
    else:
        return False
    
    db.commit()
    return True


def unassign_photo_from_slot(db: Session, file_id: str) -> bool:
    """
    Unassign photo from family_details slot
    
    Args:
        db: Database session
        file_id: File ID to unassign
    
    Returns:
        True if successful, False if error
    """
    # Find family record with this file_id
    family = db.query(FamilyDetails).filter(
        (FamilyDetails.photo_file_id_1 == file_id) |
        (FamilyDetails.photo_file_id_2 == file_id)
    ).first()
    
    if not family:
        return False
    
    # Unassign from appropriate slot
    if family.photo_file_id_1 == file_id:
        family.photo_file_id_1 = None
    elif family.photo_file_id_2 == file_id:
        family.photo_file_id_2 = None
    
    db.commit()
    return True


# ==================== COMMUNITY CERTIFICATE ASSIGNMENT ====================

def assign_community_cert_to_family(
    db: Session,
    profile_id: int,
    file_id: str
) -> Tuple[bool, Optional[str]]:
    """
    Assign community certificate file to family_details
    
    Args:
        db: Database session
        profile_id: Profile ID
        file_id: File ID to assign
    
    Returns:
        Tuple[success, error_message]
        - (True, None) if successful
        - (False, error_msg) if error (e.g., slot already taken)
    """
    family = db.query(FamilyDetails).filter(FamilyDetails.profile_id == profile_id).first()
    
    if not family:
        # Create family record if doesn't exist
        family = FamilyDetails(profile_id=profile_id)
        db.add(family)
        db.flush()
    
    # Check if community certificate already assigned
    if family.community_file_id is not None:
        return False, "Community certificate already uploaded for this profile"
    
    # Assign to community_file_id
    family.community_file_id = file_id
    db.commit()
    return True, None


def unassign_community_cert_from_family(db: Session, file_id: str) -> bool:
    """
    Unassign community certificate from family_details
    
    Args:
        db: Database session
        file_id: File ID to unassign
    
    Returns:
        True if successful, False if not found
    """
    # Find family record with this file_id
    family = db.query(FamilyDetails).filter(
        FamilyDetails.community_file_id == file_id
    ).first()
    
    if not family:
        return False
    
    # Unassign from community_file_id
    family.community_file_id = None
    db.commit()
    return True


# ==================== HELPER FUNCTIONS ====================

def get_profile_serial_number(db: Session, profile_id: int) -> Optional[str]:
    """
    Get profile serial number
    
    Args:
        db: Database session
        profile_id: Profile ID
    
    Returns:
        Serial number string or None
    """
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    return profile.serial_number if profile else None
