from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File as FastAPIFile, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.file import (
    generate_file_id, calculate_checksum, create_file, get_file_by_id, 
    get_files_by_ids, update_file, delete_file, get_files_by_kind,
    get_files_by_status, get_ready_files, get_file_versions,
    find_duplicate_by_checksum, get_file_statistics, get_large_files,
    mark_file_as_ready, mark_file_as_rejected, mark_file_as_quarantined,
    get_images_by_dimensions
)
from app.crud.file_upload import (
    create_file_record, find_duplicate_by_checksum as find_dup,
    assign_photo_to_slot, unassign_photo_from_slot,
    get_profile_serial_number, find_available_photo_slot,
    get_profile_with_family
)
from app.schemas.file import (
    FileCreate, FileUpdate, FileResponse, FileUploadRequest, 
    FileUploadResponse, FileMetadata, FileStatistics, 
    FileKindEnum, ProcessingStatusEnum
)
from app.schemas.file_upload import FileUploadResponse as PhotoUploadResponse, FileUploadErrorResponse, ErrorCodeEnum, FileDeleteResponse
from app.utils.file_handler import (
    validate_file_size, validate_mime_type, calculate_checksum as calc_checksum,
    scan_file_with_clamav, convert_to_webp, generate_thumbnail,
    ensure_directory, save_file_to_disk, delete_file_from_disk,
    generate_photo_filename
)
from typing import List, Optional
import os
import shutil
from pathlib import Path
import uuid
import io
import platform

# ==================== CONFIGURATION ====================

# Detect operating system
SYSTEM = platform.system()  # 'Windows', 'Linux', 'Darwin' (macOS)

# Define upload paths based on operating system
if SYSTEM == 'Windows':
    # Windows paths (use relative or absolute Windows paths)
    BASE_UPLOAD_DIR = Path("./uploads")  # or use: Path("C:\\uploads")
    PHOTOS_DIR = BASE_UPLOAD_DIR / "photos"
    QUARANTINE_DIR = BASE_UPLOAD_DIR / "quarantine"
    THUMBNAIL_DIR = BASE_UPLOAD_DIR / "thumbnails"
else:
    # Linux/Ubuntu paths
    BASE_UPLOAD_DIR = Path("/srv/uploads")  # or use: Path("/home/user/uploads")
    PHOTOS_DIR = BASE_UPLOAD_DIR / "photos"
    QUARANTINE_DIR = BASE_UPLOAD_DIR / "quarantine"
    THUMBNAIL_DIR = BASE_UPLOAD_DIR / "thumbnails"

# Legacy aliases for backward compatibility
UPLOAD_DIR = BASE_UPLOAD_DIR

# Create directories if they don't exist
BASE_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
PHOTOS_DIR.mkdir(parents=True, exist_ok=True)
QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)
THUMBNAIL_DIR.mkdir(parents=True, exist_ok=True)

# Print configuration for debugging
print(f"[FILE UPLOAD CONFIG] OS: {SYSTEM}")
print(f"[FILE UPLOAD CONFIG] Base Upload Dir: {BASE_UPLOAD_DIR.absolute()}")
print(f"[FILE UPLOAD CONFIG] Photos Dir: {PHOTOS_DIR.absolute()}")
print(f"[FILE UPLOAD CONFIG] Quarantine Dir: {QUARANTINE_DIR.absolute()}")
print(f"[FILE UPLOAD CONFIG] Thumbnail Dir: {THUMBNAIL_DIR.absolute()}")

router = APIRouter(prefix="/files", tags=["files"])

# ==================== FILE UPLOAD ====================

@router.post("/upload/profile-photo", response_model=PhotoUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_profile_photo(
    file: UploadFile = FastAPIFile(...),
    profile_id: int = Query(..., description="Profile ID"),
    db: Session = Depends(get_db)
):
    """
    Upload profile photo with validation, virus scanning, and WebP conversion.
    
    Purpose: Handle family photo uploads for matrimony profiles
    
    Workflow:
    1. Validate file size (max 10MB)
    2. Validate MIME type (JPEG, PNG, WebP only)
    3. Calculate SHA256 checksum for duplicate detection
    4. Check for existing duplicate file
    5. Save to quarantine directory
    6. Scan for viruses with ClamAV (with fallback to clamscan)
    7. Convert to WebP with EXIF preservation
    8. Generate thumbnail (150x150 WebP)
    9. Determine available photo slot (1 or 2)
    10. Move file to permanent storage
    11. Create database record
    12. Assign to family_details photo slot
    13. Return FileUploadResponse with file_id and thumbnail_url
    
    Error Handling:
    - SIZE_EXCEEDED: File > 10MB
    - VIRUS_FOUND: Virus detected during scan
    - INVALID_FILE_TYPE: Not JPEG, PNG, or WebP
    - DUPLICATE_DETECTED: Identical file already exists
    - NO_FREE_SLOT: Already have 2 photos (max allowed)
    - PROCESSING_ERROR: Conversion or storage failed
    
    Security:
    - File size validation (10MB limit)
    - MIME type whitelist (image/jpeg, image/png, image/webp only)
    - SHA256 duplicate detection
    - ClamAV virus scanning with fallback
    - EXIF data preserved (important for image metadata)
    - WebP conversion for efficient storage
    
    Returns:
    - Success: {status: 'success', file_id, thumbnail_url, profile_id}
    - Error: {status: 'error', code: ErrorCodeEnum, message: str}
    """
    try:
        # Get profile to verify it exists and get serial number
        profile, family = get_profile_with_family(db, profile_id)
        if not profile:
            return PhotoUploadResponse(
                status="error",
                code=ErrorCodeEnum.NOT_FOUND,
                message=f"Profile {profile_id} not found"
            )

        # Read file content
        file_content = await file.read()
        if not file_content:
            return PhotoUploadResponse(
                status="error",
                code=ErrorCodeEnum.PROCESSING_ERROR,
                message="File is empty"
            )

        # Validate file size (10MB max for images)
        size_ok, size_error = validate_file_size(file_content, max_size_mb=10)
        if not size_ok:
            print(f"[UPLOAD PHOTO] File size validation failed: {size_error}")
            return PhotoUploadResponse(
                status="error",
                code=ErrorCodeEnum.SIZE_EXCEEDED,
                message=size_error
            )

        # Validate MIME type (only JPEG, PNG, WebP)
        allowed_mimes = ['image/jpeg', 'image/png', 'image/webp']
        mime_ok, mime_error = validate_mime_type(file.content_type, allowed_types=allowed_mimes)
        if not mime_ok:
            return PhotoUploadResponse(
                status="error",
                code=ErrorCodeEnum.INVALID_FILE_TYPE,
                message=mime_error
            )

        # Calculate checksum for duplicate detection
        checksum = calc_checksum(file_content)
        if not checksum:
            return PhotoUploadResponse(
                status="error",
                code=ErrorCodeEnum.PROCESSING_ERROR,
                message="Failed to calculate checksum"
            )

        # Check for existing duplicate file
        existing_file = find_dup(db, checksum)
        if existing_file:
            # Return existing file's ID instead of creating duplicate
            thumbnail_url = f"/files/{existing_file.id}/thumbnail" if existing_file.thumbnail_path else None
            return PhotoUploadResponse(
                status="success",
                file_id=existing_file.id,
                thumbnail_url=thumbnail_url,
                profile_id=profile_id,
                message="File already exists (duplicate detected)"
            )

        # Generate unique file ID
        file_id = str(uuid.uuid4())
        
        # Create directories (ensure they exist)
        quarantine_dir = QUARANTINE_DIR
        ensure_directory(str(quarantine_dir))
        
        photos_dir = PHOTOS_DIR
        ensure_directory(str(photos_dir))
        
        thumbnails_dir = THUMBNAIL_DIR
        ensure_directory(str(thumbnails_dir))
        
        # Save to quarantine directory first
        quarantine_path = str(quarantine_dir / f"{file_id}.bin")
        saved, save_error = save_file_to_disk(file_content, quarantine_path)
        if not saved:
            return PhotoUploadResponse(
                status="error",
                code=ErrorCodeEnum.PROCESSING_ERROR,
                message=f"Failed to save file: {save_error}"
            )

        # Scan for viruses
        clean, virus_error = scan_file_with_clamav(quarantine_path)
        if not clean:
            # Delete quarantined file
            _, _ = delete_file_from_disk(quarantine_path)
            return PhotoUploadResponse(
                status="error",
                code=ErrorCodeEnum.VIRUS_FOUND,
                message=virus_error or "Virus detected"
            )

        # Convert to WebP and preserve EXIF
        webp_bytes, convert_error = convert_to_webp(file_content, quality=85)
        if convert_error or not webp_bytes:
            _, _ = delete_file_from_disk(quarantine_path)
            return PhotoUploadResponse(
                status="error",
                code=ErrorCodeEnum.PROCESSING_ERROR,
                message=f"Failed to convert to WebP: {convert_error}"
            )

        # Generate thumbnail
        thumb_bytes, thumb_error = generate_thumbnail(webp_bytes, size=(150, 150))
        if thumb_error or not thumb_bytes:
            _, _ = delete_file_from_disk(quarantine_path)
            return PhotoUploadResponse(
                status="error",
                code=ErrorCodeEnum.PROCESSING_ERROR,
                message=f"Failed to generate thumbnail: {thumb_error}"
            )

        # Find available photo slot (1 or 2)
        slot_num, slot_error = find_available_photo_slot(db, profile_id)
        if slot_error:
            _, _ = delete_file_from_disk(quarantine_path)
            return PhotoUploadResponse(
                status="error",
                code=ErrorCodeEnum.NO_FREE_SLOT,
                message=slot_error
            )

        # Generate filename: {serial_number}_photo_{slot}.webp
        serial_number = profile.serial_number
        if not serial_number:
            serial_number = str(profile.id)

        filename = f"{serial_number}_photo_{slot_num}.webp"
        storage_path = str(photos_dir / filename)
        thumbnail_path = str(thumbnails_dir / f"{serial_number}_photo_{slot_num}_thumb.webp")

        # Save WebP file to permanent storage
        saved, save_error = save_file_to_disk(webp_bytes, storage_path)
        if not saved:
            _, _ = delete_file_from_disk(quarantine_path)
            return PhotoUploadResponse(
                status="error",
                code=ErrorCodeEnum.PROCESSING_ERROR,
                message=f"Failed to save WebP file: {save_error}"
            )

        # Save thumbnail
        saved, save_error = save_file_to_disk(thumb_bytes, thumbnail_path)
        if not saved:
            _, _ = delete_file_from_disk(quarantine_path)
            _, _ = delete_file_from_disk(storage_path)
            return PhotoUploadResponse(
                status="error",
                code=ErrorCodeEnum.PROCESSING_ERROR,
                message=f"Failed to save thumbnail: {save_error}"
            )

        # Delete quarantine file (no longer needed)
        _, _ = delete_file_from_disk(quarantine_path)
        
        # Create database file record
        from app.models.file import File, FileKindEnum as ModelFileKindEnum, ProcessingStatusEnum as ModelStatusEnum
        
        try:
            file_obj = File(
                id=file_id,
                original_name=file.filename or "photo.webp",
                file_kind=ModelFileKindEnum.image,
                storage_path=storage_path,
                thumbnail_path=thumbnail_path,
                mime_type="image/webp",
                size_bytes=len(webp_bytes),
                checksum=checksum,
                processing_status=ModelStatusEnum.ready
            )
            db.add(file_obj)
            db.commit()
            db.refresh(file_obj)
        except Exception as e:
            # Cleanup on DB error
            _, _ = delete_file_from_disk(storage_path)
            _, _ = delete_file_from_disk(thumbnail_path)
            return PhotoUploadResponse(
                status="error",
                code=ErrorCodeEnum.PROCESSING_ERROR,
                message=f"Failed to create database record: {str(e)}"
            )
        
        # Assign to family_details photo slot
        assigned = assign_photo_to_slot(db, profile_id, file_id, slot_num)
        if not assigned:
            # Cleanup on assignment error
            _, _ = delete_file_from_disk(storage_path)
            _, _ = delete_file_from_disk(thumbnail_path)
            db.delete(file_obj)
            db.commit()
            return PhotoUploadResponse(
                status="error",
                code=ErrorCodeEnum.PROCESSING_ERROR,
                message="Failed to assign photo slot"
            )
        
        # Success response
        thumbnail_url = f"/files/{file_id}/thumbnail"
        return PhotoUploadResponse(
            status="success",
            file_id=file_id,
            thumbnail_url=thumbnail_url,
            profile_id=profile_id,
            message="Photo uploaded successfully"
        )
    
    except Exception as e:
        return PhotoUploadResponse(
            status="error",
            code=ErrorCodeEnum.PROCESSING_ERROR,
            message=f"Unexpected error: {str(e)}"
        )


@router.delete("/{file_id}", response_model=FileDeleteResponse)
async def delete_profile_photo(
    file_id: str,
    profile_id: int = Query(..., description="Profile ID"),
    db: Session = Depends(get_db)
):
    """
    Delete profile photo and unassign from family_details.
    
    Purpose: Remove photo from profile with cleanup
    
    Workflow:
    1. Get file record by ID
    2. Verify file exists
    3. Verify file belongs to profile (optional but recommended)
    4. Delete physical file from disk
    5. Delete thumbnail from disk
    6. Unassign from family_details photo slot
    7. Delete database file record
    8. Return success response
    
    Error Handling:
    - NOT_FOUND: File not found
    - PROCESSING_ERROR: Disk deletion failed
    
    Returns:
    - Success: {status: 'success', file_id, message}
    - Error: {status: 'error', code: ErrorCodeEnum, message: str}
    """
    try:
        from app.models.file import File
        
        # Get file record
        db_file = db.query(File).filter(File.id == file_id).first()
        if not db_file:
            return FileDeleteResponse(
                status="error",
                code=ErrorCodeEnum.NOT_FOUND,
                message=f"File {file_id} not found"
            )
        
        # Delete physical file from storage
        if db_file.storage_path and os.path.exists(db_file.storage_path):
            try:
                _, _ = delete_file_from_disk(db_file.storage_path)
            except Exception as e:
                return FileDeleteResponse(
                    status="error",
                    code=ErrorCodeEnum.PROCESSING_ERROR,
                    message=f"Failed to delete file from disk: {str(e)}"
                )
        
        # Delete thumbnail
        if db_file.thumbnail_path and os.path.exists(db_file.thumbnail_path):
            try:
                _, _ = delete_file_from_disk(db_file.thumbnail_path)
            except Exception as e:
                # Non-fatal, continue with deletion
                print(f"Warning: Failed to delete thumbnail: {e}")
        
        # Unassign from family_details
        unassigned = unassign_photo_from_slot(db, file_id)
        if not unassigned:
            # Still delete the file record even if unassignment failed
            print(f"Warning: Failed to unassign photo slot")
        
        # Delete database record
        db.delete(db_file)
        db.commit()
        
        return FileDeleteResponse(
            status="success",
            file_id=file_id,
            message="Photo deleted successfully"
        )
    
    except Exception as e:
        return FileDeleteResponse(
            status="error",
            code=ErrorCodeEnum.PROCESSING_ERROR,
            message=f"Unexpected error during deletion: {str(e)}"
        )



@router.get("/{file_id}/thumbnail")
def get_thumbnail(file_id: str, db: Session = Depends(get_db)):
    """
    Get file thumbnail
    
    Purpose: Serve thumbnail for image preview
    
    Use Cases:
    - Gallery thumbnails
    - Profile photo preview
    - PDF first page preview
    """
    from fastapi.responses import FileResponse
    
    db_file = get_file_by_id(db, file_id)
    
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    
    if not db_file.thumbnail_path:
        raise HTTPException(status_code=404, detail="Thumbnail not available")
    
    if not os.path.exists(db_file.thumbnail_path):
        raise HTTPException(status_code=404, detail="Thumbnail not found on disk")
    
    return FileResponse(
        path=db_file.thumbnail_path,
        media_type="image/webp"
    )


# ==================== STATISTICS & ADMIN ====================

@router.get("/admin/statistics", response_model=FileStatistics)
def get_statistics(db: Session = Depends(get_db)):
    """
    Get file system statistics
    
    Purpose: Admin dashboard metrics
    
    Returns:
    - Total files
    - Total storage used
    - Files by kind
    - Files by status
    - Pending/rejected counts
    """
    stats = get_file_statistics(db)
    
    return FileStatistics(
        total_files=stats["total_files"],
        total_size_bytes=stats["total_size_bytes"],
        total_size_mb=stats["total_size_mb"],
        files_by_kind=stats["files_by_kind"],
        files_by_status=stats["files_by_status"],
        pending_files=stats["pending_files"],
        rejected_files=stats["rejected_files"]
    )

