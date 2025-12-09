from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File as FastAPIFile
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
from app.schemas.file import (
    FileCreate, FileUpdate, FileResponse, FileUploadRequest, 
    FileUploadResponse, FileMetadata, FileStatistics, 
    FileKindEnum, ProcessingStatusEnum
)
from typing import List, Optional
import os
import shutil
from pathlib import Path

router = APIRouter(prefix="/files", tags=["files"])

# Configuration
UPLOAD_DIR = Path("./uploads")  # Base upload directory
THUMBNAIL_DIR = Path("./thumbnails")  # Thumbnail storage
UPLOAD_DIR.mkdir(exist_ok=True)
THUMBNAIL_DIR.mkdir(exist_ok=True)

# ==================== FILE UPLOAD ====================

@router.post("/upload", response_model=FileResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = FastAPIFile(...),
    db: Session = Depends(get_db)
):
    """
    Upload file
    
    Purpose: Handle file upload with metadata creation
    
    Workflow:
    1. Generate UUID for file
    2. Validate file type (image or PDF)
    3. Calculate checksum (duplicate detection)
    4. Check for duplicates
    5. Save file to storage
    6. Create database record
    7. Trigger background processing (virus scan, thumbnail)
    
    Security:
    - Validate file type (whitelist only)
    - Limit file size (10MB for images, 50MB for PDFs)
    - Virus scan (integrate ClamAV or similar)
    - Content moderation for images
    
    Use Cases:
    - Profile photo upload
    - Horoscope PDF upload
    - Document upload
    
    Example Request:
    POST /files/upload
    Content-Type: multipart/form-data
    file: [binary data]
    """
    # Generate UUID
    file_id = generate_file_id()
    
    # Read file content
    file_content = await file.read()
    file_size = len(file_content)
    
    # Validate file size (10MB max for images, 50MB for PDFs)
    max_size = 50 * 1024 * 1024  # 50MB
    if file_size > max_size:
        raise HTTPException(status_code=400, detail=f"File too large (max {max_size} bytes)")
    
    # Determine file kind from mime type
    mime_type = file.content_type
    if mime_type.startswith('image/'):
        file_kind = FileKindEnum.image
        max_size = 10 * 1024 * 1024  # 10MB for images
    elif mime_type == 'application/pdf':
        file_kind = FileKindEnum.pdf
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type (only images and PDFs allowed)")
    
    # Calculate checksum
    checksum = calculate_checksum(file_content)
    
    # Check for duplicates
    duplicate = find_duplicate_by_checksum(db, checksum)
    if duplicate:
        return duplicate  # Return existing file instead of creating duplicate
    
    # Create storage path: /uploads/YYYY/MM/uuid.ext
    from datetime import datetime
    now = datetime.now()
    year_month_dir = UPLOAD_DIR / str(now.year) / f"{now.month:02d}"
    year_month_dir.mkdir(parents=True, exist_ok=True)
    
    file_extension = Path(file.filename).suffix
    storage_path = str(year_month_dir / f"{file_id}{file_extension}")
    
    # Save file to disk
    with open(storage_path, 'wb') as f:
        f.write(file_content)
    
    # Extract image dimensions (if image)
    width, height = None, None
    if file_kind == FileKindEnum.image:
        try:
            from PIL import Image
            import io
            img = Image.open(io.BytesIO(file_content))
            width, height = img.size
        except Exception as e:
            print(f"Could not extract image dimensions: {e}")
    
    # Create database record
    file_data = FileCreate(
        id=file_id,
        original_name=file.filename,
        file_kind=file_kind,
        storage_path=storage_path,
        mime_type=mime_type,
        size_bytes=file_size,
        checksum=checksum,
        width=width,
        height=height,
        processing_status=ProcessingStatusEnum.pending
    )
    
    db_file = create_file(db, file_data)
    
    # TODO: Trigger background processing
    # - Virus scan (ClamAV)
    # - Content moderation (AWS Rekognition, Google Vision AI)
    # - Thumbnail generation (if image)
    # - OCR (if PDF)
    
    return db_file

@router.post("/initiate-upload", response_model=FileUploadResponse)
def initiate_upload(
    request: FileUploadRequest,
    db: Session = Depends(get_db)
):
    """
    Initiate file upload (for S3 presigned URLs)
    
    Purpose: Get presigned URL for direct S3 upload
    
    Workflow:
    1. Validate file metadata
    2. Generate UUID
    3. Generate presigned URL (if using S3)
    4. Return upload URL to client
    5. Client uploads directly to S3
    6. Client calls /confirm-upload after upload complete
    
    Use Cases:
    - Large file uploads (avoid server proxy)
    - Mobile app uploads
    - Better performance (direct to S3)
    """
    file_id = generate_file_id()
    
    # TODO: Generate S3 presigned URL
    # import boto3
    # s3 = boto3.client('s3')
    # presigned_url = s3.generate_presigned_url(
    #     'put_object',
    #     Params={'Bucket': 'my-bucket', 'Key': file_id},
    #     ExpiresIn=3600
    # )
    
    # For now, return local upload URL
    upload_url = f"/files/upload"
    
    return FileUploadResponse(
        file_id=file_id,
        upload_url=upload_url,
        message="Use this file_id for upload confirmation"
    )

# ==================== FILE RETRIEVAL ====================

@router.get("/{file_id}", response_model=FileResponse)
def get_file(file_id: str, db: Session = Depends(get_db)):
    """
    Get file by ID
    
    Purpose: Retrieve file metadata
    """
    db_file = get_file_by_id(db, file_id)
    
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    
    return db_file

@router.get("/{file_id}/download")
def download_file(file_id: str, db: Session = Depends(get_db)):
    """
    Download file
    
    Purpose: Serve file for download
    
    Security:
    - Check processing_status (only serve 'ready' files)
    - Verify user permissions (if file is private)
    - Log downloads for audit
    """
    from fastapi.responses import FileResponse
    
    db_file = get_file_by_id(db, file_id)
    
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    
    if db_file.processing_status != ProcessingStatusEnum.ready:
        raise HTTPException(status_code=403, detail="File not ready for download")
    
    if not os.path.exists(db_file.storage_path):
        raise HTTPException(status_code=404, detail="File not found on disk")
    
    return FileResponse(
        path=db_file.storage_path,
        filename=db_file.original_name,
        media_type=db_file.mime_type
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
        media_type="image/jpeg"
    )

# ==================== FILE MANAGEMENT ====================

@router.patch("/{file_id}", response_model=FileResponse)
def update_file_metadata(
    file_id: str,
    file_data: FileUpdate,
    db: Session = Depends(get_db)
):
    """
    Update file metadata
    
    Purpose: Update processing status, paths, etc.
    
    Use Cases:
    - Virus scan complete → update status to 'ready'
    - Thumbnail generated → update thumbnail_path
    - Admin review → update status to 'rejected' or 'quarantined'
    """
    db_file = update_file(db, file_id, file_data)
    
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    
    return db_file

@router.delete("/{file_id}")
def delete_file_endpoint(file_id: str, db: Session = Depends(get_db)):
    """
    Delete file
    
    Purpose: Remove file from system
    
    Security:
    - Verify user permissions
    - Soft delete (keep record for audit)
    - Delete physical file from storage
    - Delete thumbnails
    
    Use Cases:
    - User deletes uploaded photo
    - Admin removes inappropriate content
    - Cleanup old files
    """
    db_file = get_file_by_id(db, file_id)
    
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Delete physical file
    if os.path.exists(db_file.storage_path):
        os.remove(db_file.storage_path)
    
    # Delete thumbnail
    if db_file.thumbnail_path and os.path.exists(db_file.thumbnail_path):
        os.remove(db_file.thumbnail_path)
    
    # Delete database record
    delete_file(db, file_id)
    
    return {"success": True, "message": "File deleted successfully"}

# ==================== FILTERING & SEARCH ====================

@router.get("/kind/{file_kind}", response_model=List[FileMetadata])
def get_files_by_kind_endpoint(
    file_kind: FileKindEnum,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get files by kind (image or pdf)
    
    Purpose: Filter files by type
    
    Use Cases:
    - Show all images in gallery
    - List all PDF documents
    """
    files = get_files_by_kind(db, file_kind, skip, limit)
    
    return [
        FileMetadata(
            id=f.id,
            original_name=f.original_name,
            file_kind=f.file_kind,
            size_bytes=f.size_bytes,
            processing_status=f.processing_status,
            created_at=f.created_at,
            thumbnail_url=f"/files/{f.id}/thumbnail" if f.thumbnail_path else None
        )
        for f in files
    ]

@router.get("/status/{status}", response_model=List[FileResponse])
def get_files_by_status_endpoint(
    status: ProcessingStatusEnum,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get files by processing status
    
    Purpose: Workflow management
    
    Use Cases:
    - Admin: Review pending files
    - Admin: Review quarantined files
    - System: Process pending files
    """
    return get_files_by_status(db, status, skip, limit)

@router.get("/ready/list", response_model=List[FileMetadata])
def get_ready_files_endpoint(
    file_kind: Optional[FileKindEnum] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get approved files ready for use
    
    Purpose: Show only approved files
    
    Use Cases:
    - Gallery display (only show ready images)
    - Document downloads (only allow ready PDFs)
    """
    files = get_ready_files(db, file_kind, skip, limit)
    
    return [
        FileMetadata(
            id=f.id,
            original_name=f.original_name,
            file_kind=f.file_kind,
            size_bytes=f.size_bytes,
            processing_status=f.processing_status,
            created_at=f.created_at,
            thumbnail_url=f"/files/{f.id}/thumbnail" if f.thumbnail_path else None
        )
        for f in files
    ]

# ==================== VERSIONING ====================

@router.get("/{file_id}/versions", response_model=List[FileResponse])
def get_file_versions_endpoint(file_id: str, db: Session = Depends(get_db)):
    """
    Get all versions of a file
    
    Purpose: Show file revision history
    
    Use Cases:
    - User uploads new horoscope (version 2)
    - Show version history
    - Rollback to previous version
    """
    return get_file_versions(db, file_id)

# ==================== PROCESSING WORKFLOW ====================

@router.post("/{file_id}/approve")
def approve_file(file_id: str, db: Session = Depends(get_db)):
    """
    Approve file (mark as ready)
    
    Purpose: Admin approves file after review
    
    Workflow:
    1. Admin reviews file
    2. Admin approves (no issues found)
    3. Status updated to 'ready'
    4. File becomes visible to users
    """
    db_file = mark_file_as_ready(db, file_id)
    
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    
    return {"success": True, "message": "File approved", "file_id": file_id}

@router.post("/{file_id}/reject")
def reject_file(file_id: str, reason: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Reject file
    
    Purpose: Admin rejects inappropriate file
    
    Reasons:
    - Inappropriate content
    - Violates terms of service
    - Low quality
    - Spam
    """
    db_file = mark_file_as_rejected(db, file_id, reason)
    
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    
    return {"success": True, "message": "File rejected", "file_id": file_id}

@router.post("/{file_id}/quarantine")
def quarantine_file(file_id: str, db: Session = Depends(get_db)):
    """
    Quarantine file for manual review
    
    Purpose: Flag suspicious file
    
    Triggers:
    - Content moderation flagged
    - User report
    - Suspicious patterns
    """
    db_file = mark_file_as_quarantined(db, file_id)
    
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    
    return {"success": True, "message": "File quarantined", "file_id": file_id}

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

@router.get("/admin/large-files", response_model=List[FileResponse])
def get_large_files_endpoint(
    min_size_mb: int = 10,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get large files
    
    Purpose: Identify files consuming storage
    
    Use Cases:
    - Storage optimization
    - Find files to compress
    - Admin cleanup
    """
    return get_large_files(db, min_size_mb, skip, limit)

# ==================== IMAGE-SPECIFIC ====================

@router.get("/images/dimensions", response_model=List[FileResponse])
def get_images_by_dimensions_endpoint(
    min_width: Optional[int] = None,
    max_width: Optional[int] = None,
    min_height: Optional[int] = None,
    max_height: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get images by dimension constraints
    
    Purpose: Filter images by size
    
    Use Cases:
    - Find high-resolution images (width > 1920)
    - Find portrait vs landscape images
    - Quality control
    
    Example:
    GET /files/images/dimensions?min_width=1920&min_height=1080
    """
    return get_images_by_dimensions(db, min_width, max_width, min_height, max_height, skip, limit)
