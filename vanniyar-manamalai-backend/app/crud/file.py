from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from ..models.file import File, FileKindEnum, ProcessingStatusEnum
from ..schemas.file import FileCreate, FileUpdate
from fastapi import HTTPException
import uuid
import hashlib
from typing import Optional, List

def generate_file_id() -> str:
    """Generate UUID v4 for file ID"""
    return str(uuid.uuid4())

def calculate_checksum(file_bytes: bytes) -> str:
    """Calculate SHA256 checksum"""
    return hashlib.sha256(file_bytes).hexdigest()

def create_file(db: Session, file_data: FileCreate):
    """
    Create file record in database
    
    Purpose: Register uploaded file in system
    
    Workflow:
    1. Generate UUID for file
    2. Calculate checksum (integrity verification)
    3. Store file metadata
    4. Set initial status to 'pending'
    5. Trigger background processing (virus scan, thumbnail generation)
    """
    db_file = File(**file_data.dict())
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def get_file_by_id(db: Session, file_id: str):
    """Get file by ID"""
    return db.query(File).filter(File.id == file_id).first()

def get_files_by_ids(db: Session, file_ids: List[str]):
    """
    Get multiple files by IDs
    
    Purpose: Batch retrieval for gallery display
    """
    return db.query(File).filter(File.id.in_(file_ids)).all()

def update_file(db: Session, file_id: str, file_data: FileUpdate):
    """
    Update file metadata
    
    Purpose: Update processing status, add thumbnail path, etc.
    
    Use Cases:
    - Virus scan complete → update status to 'ready'
    - Thumbnail generated → update thumbnail_path
    - Content moderation → update status to 'quarantined' or 'rejected'
    """
    db_file = db.query(File).filter(File.id == file_id).first()
    
    if not db_file:
        return None
    
    update_data = file_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_file, field, value)
    
    db.commit()
    db.refresh(db_file)
    return db_file

def delete_file(db: Session, file_id: str):
    """
    Delete file record (soft delete - keeps record but marks as deleted)
    
    Purpose: Remove file from system
    
    Note: Should also delete physical file from storage
    """
    db_file = db.query(File).filter(File.id == file_id).first()
    
    if not db_file:
        return None
    
    db.delete(db_file)
    db.commit()
    return db_file

# ==================== FILTERING & SEARCH ====================

def get_files_by_kind(db: Session, file_kind: FileKindEnum, skip: int = 0, limit: int = 100):
    """
    Get files by kind (image or pdf)
    
    Purpose: Filter files by type
    
    Use Cases:
    - Show all images in gallery
    - List all PDF documents
    """
    return (
        db.query(File)
        .filter(File.file_kind == file_kind)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_files_by_status(db: Session, status: ProcessingStatusEnum, skip: int = 0, limit: int = 100):
    """
    Get files by processing status
    
    Purpose: Workflow management
    
    Use Cases:
    - Show pending files (awaiting processing)
    - Show quarantined files (admin review needed)
    - Show rejected files (inappropriate content)
    """
    return (
        db.query(File)
        .filter(File.processing_status == status)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_ready_files(db: Session, file_kind: Optional[FileKindEnum] = None, skip: int = 0, limit: int = 100):
    """
    Get files ready for use
    
    Purpose: Show approved files only
    
    Use Cases:
    - Gallery display (only show ready images)
    - Document downloads (only allow ready PDFs)
    """
    query = db.query(File).filter(File.processing_status == ProcessingStatusEnum.ready)
    
    if file_kind:
        query = query.filter(File.file_kind == file_kind)
    
    return query.offset(skip).limit(limit).all()

def get_files_by_original_name(db: Session, original_name: str, skip: int = 0, limit: int = 100):
    """
    Search files by original filename
    
    Purpose: Find files by name
    
    Use Cases:
    - User searches "horoscope.pdf"
    - Find specific uploaded file
    """
    return (
        db.query(File)
        .filter(File.original_name.ilike(f"%{original_name}%"))
        .offset(skip)
        .limit(limit)
        .all()
    )

# ==================== VERSIONING ====================

def get_file_versions(db: Session, file_id: str):
    """
    Get all versions of a file
    
    Purpose: Track file revision history
    
    Use Cases:
    - User uploads new horoscope (version 2)
    - Show version history
    - Rollback to previous version
    
    Returns: List of files where version_of = file_id (newer versions)
    """
    return (
        db.query(File)
        .filter(File.version_of == file_id)
        .order_by(File.created_at.desc())
        .all()
    )

def get_latest_version(db: Session, file_id: str):
    """
    Get latest version of a file
    
    Purpose: Always use most recent file version
    
    Workflow:
    1. Start with original file_id
    2. Check if newer versions exist (version_of = file_id)
    3. Return latest version
    """
    latest = db.query(File).filter(File.version_of == file_id).order_by(File.created_at.desc()).first()
    
    if latest:
        return latest
    else:
        # No newer version, return original
        return db.query(File).filter(File.id == file_id).first()

# ==================== DUPLICATE DETECTION ====================

def find_duplicate_by_checksum(db: Session, checksum: str):
    """
    Find duplicate files by checksum
    
    Purpose: Prevent storing identical files
    
    Use Cases:
    - User uploads same photo twice
    - Deduplication (save storage space)
    - Detect re-uploads
    
    Returns: First file with matching checksum
    """
    return db.query(File).filter(File.checksum == checksum).first()

def find_duplicates_by_size_and_name(db: Session, size_bytes: int, original_name: str):
    """
    Find potential duplicates by size and name
    
    Purpose: Fast duplicate detection before checksum calculation
    
    Use Cases:
    - Quick duplicate check during upload
    - Find similar files
    """
    return (
        db.query(File)
        .filter(
            and_(
                File.size_bytes == size_bytes,
                File.original_name == original_name
            )
        )
        .all()
    )

# ==================== STATISTICS & ADMIN ====================

def get_file_statistics(db: Session):
    """
    Get file system statistics
    
    Purpose: Admin dashboard metrics
    
    Returns:
    - Total files
    - Total storage used
    - Files by kind (image/pdf)
    - Files by status (pending/ready/rejected)
    """
    total_files = db.query(func.count(File.id)).scalar()
    total_size = db.query(func.sum(File.size_bytes)).scalar() or 0
    
    # Files by kind
    files_by_kind = {}
    for kind in FileKindEnum:
        count = db.query(func.count(File.id)).filter(File.file_kind == kind.value).scalar()
        files_by_kind[kind.value] = count
    
    # Files by status
    files_by_status = {}
    for status in ProcessingStatusEnum:
        count = db.query(func.count(File.id)).filter(File.processing_status == status.value).scalar()
        files_by_status[status.value] = count
    
    return {
        "total_files": total_files,
        "total_size_bytes": total_size,
        "total_size_mb": round(total_size / (1024 * 1024), 2),
        "files_by_kind": files_by_kind,
        "files_by_status": files_by_status,
        "pending_files": files_by_status.get("pending", 0),
        "rejected_files": files_by_status.get("rejected", 0)
    }

def get_large_files(db: Session, min_size_mb: int = 10, skip: int = 0, limit: int = 100):
    """
    Get large files
    
    Purpose: Identify files consuming storage
    
    Use Cases:
    - Storage optimization
    - Find files to compress
    - Admin cleanup
    """
    min_size_bytes = min_size_mb * 1024 * 1024
    
    return (
        db.query(File)
        .filter(File.size_bytes >= min_size_bytes)
        .order_by(File.size_bytes.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_files_without_checksum(db: Session, skip: int = 0, limit: int = 100):
    """
    Get files missing checksum
    
    Purpose: Find files needing checksum calculation
    
    Use Cases:
    - Background job to calculate missing checksums
    - Data integrity verification
    """
    return (
        db.query(File)
        .filter(File.checksum.is_(None))
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_orphaned_thumbnails(db: Session):
    """
    Get files with thumbnail_path but no actual thumbnail
    
    Purpose: Cleanup orphaned references
    
    Note: Requires filesystem check (not just DB query)
    """
    return (
        db.query(File)
        .filter(File.thumbnail_path.isnot(None))
        .all()
    )

# ==================== PROCESSING WORKFLOW ====================

def mark_file_as_ready(db: Session, file_id: str):
    """
    Mark file as ready after successful processing
    
    Purpose: Approve file for use
    
    Workflow:
    1. Virus scan passed
    2. Content moderation approved
    3. Thumbnail generated (if image)
    4. Mark as 'ready'
    """
    return update_file(db, file_id, FileUpdate(processing_status=ProcessingStatusEnum.ready))

def mark_file_as_rejected(db: Session, file_id: str, reason: str = None):
    """
    Mark file as rejected
    
    Purpose: Block inappropriate files
    
    Reasons:
    - Virus detected
    - Inappropriate content
    - Terms of service violation
    """
    # In production, store rejection reason in separate table
    return update_file(db, file_id, FileUpdate(processing_status=ProcessingStatusEnum.rejected))

def mark_file_as_quarantined(db: Session, file_id: str):
    """
    Quarantine file for manual review
    
    Purpose: Flag suspicious files
    
    Triggers:
    - Content moderation flagged
    - Suspicious file type
    - Large file size
    - User reports
    """
    return update_file(db, file_id, FileUpdate(processing_status=ProcessingStatusEnum.quarantined))

# ==================== IMAGE-SPECIFIC ====================

def get_images_by_dimensions(
    db: Session, 
    min_width: Optional[int] = None,
    max_width: Optional[int] = None,
    min_height: Optional[int] = None,
    max_height: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
):
    """
    Get images by dimension constraints
    
    Purpose: Filter images by size
    
    Use Cases:
    - Find high-resolution images (width > 1920)
    - Find portrait vs landscape images
    - Quality control
    """
    query = db.query(File).filter(File.file_kind == FileKindEnum.image)
    
    if min_width:
        query = query.filter(File.width >= min_width)
    if max_width:
        query = query.filter(File.width <= max_width)
    if min_height:
        query = query.filter(File.height >= min_height)
    if max_height:
        query = query.filter(File.height <= max_height)
    
    return query.offset(skip).limit(limit).all()
