from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from enum import Enum

class FileKindEnum(str, Enum):
    """File type categories"""
    image = "image"
    pdf = "pdf"

class ProcessingStatusEnum(str, Enum):
    """File processing workflow states"""
    pending = "pending"
    quarantined = "quarantined"
    scanning = "scanning"
    ready = "ready"
    rejected = "rejected"

class FileBase(BaseModel):
    """Base file schema"""
    original_name: str = Field(..., max_length=512, description="Original filename")
    file_kind: FileKindEnum
    storage_path: str = Field(..., max_length=768, description="Filesystem storage path")
    mime_type: str = Field(..., max_length=128, description="MIME type (e.g., image/jpeg)")
    size_bytes: int = Field(..., ge=0, description="File size in bytes")
    checksum: Optional[str] = Field(default=None, max_length=64, description="SHA256 hash")
    width: Optional[int] = Field(default=None, ge=0, description="Image width in pixels")
    height: Optional[int] = Field(default=None, ge=0, description="Image height in pixels")
    thumbnail_path: Optional[str] = Field(default=None, max_length=768, description="Thumbnail path")
    candidate_pdf_path: Optional[str] = Field(default=None, max_length=768, description="Candidate PDF path")
    processing_status: ProcessingStatusEnum = ProcessingStatusEnum.pending
    version_of: Optional[str] = Field(default=None, max_length=36, description="Previous file ID (versioning)")

    @validator('mime_type')
    def validate_mime_type(cls, v, values):
        """Ensure mime_type matches file_kind"""
        if 'file_kind' in values:
            file_kind = values['file_kind']
            if file_kind == FileKindEnum.image and not v.startswith('image/'):
                raise ValueError('mime_type must start with "image/" for image file_kind')
            if file_kind == FileKindEnum.pdf and v != 'application/pdf':
                raise ValueError('mime_type must be "application/pdf" for pdf file_kind')
        return v

class FileCreate(FileBase):
    """Schema for creating file record"""
    id: str = Field(..., max_length=36, description="UUID v4")

class FileUpdate(BaseModel):
    """Schema for updating file record"""
    processing_status: Optional[ProcessingStatusEnum] = None
    thumbnail_path: Optional[str] = None
    candidate_pdf_path: Optional[str] = None
    checksum: Optional[str] = None

class FileResponse(FileBase):
    """Schema for file responses"""
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True

class FileUploadRequest(BaseModel):
    """Schema for file upload initiation"""
    original_name: str
    file_kind: FileKindEnum
    mime_type: str
    size_bytes: int

class FileUploadResponse(BaseModel):
    """Response after file upload"""
    file_id: str
    upload_url: str  # Presigned URL for upload (if using S3)
    message: str

class FileMetadata(BaseModel):
    """File metadata summary"""
    id: str
    original_name: str
    file_kind: FileKindEnum
    size_bytes: int
    processing_status: ProcessingStatusEnum
    created_at: datetime
    thumbnail_url: Optional[str] = None

class FileStatistics(BaseModel):
    """File system statistics"""
    total_files: int
    total_size_bytes: int
    total_size_mb: float
    files_by_kind: dict  # {"image": 150, "pdf": 50}
    files_by_status: dict  # {"ready": 180, "pending": 20}
    pending_files: int
    rejected_files: int
