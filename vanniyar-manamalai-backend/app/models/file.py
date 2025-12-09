from sqlalchemy import Column, String, BigInteger, Integer, ForeignKey, Enum, DateTime, CheckConstraint, Index
from sqlalchemy.sql import func
from app.database import Base
import enum

class FileKindEnum(str, enum.Enum):
    """File type categories"""
    image = "image"
    pdf = "pdf"

class ProcessingStatusEnum(str, enum.Enum):
    """File processing workflow states"""
    pending = "pending"           # Uploaded, awaiting processing
    quarantined = "quarantined"   # Flagged for review (virus scan, content moderation)
    scanning = "scanning"         # Currently being scanned/processed
    ready = "ready"               # Approved and ready for use
    rejected = "rejected"         # Rejected (inappropriate content, virus detected)

class File(Base):
    __tablename__ = "files"
    __table_args__ = (
        # Constraint: Ensure file_kind matches mime_type
        CheckConstraint(
            "(file_kind = 'image' AND mime_type LIKE 'image/%') OR "
            "(file_kind = 'pdf' AND mime_type = 'application/pdf')",
            name="chk_filekind_mime"
        ),
        # Index for fast filtering by file_kind and status
        Index('idx_filekind_status', 'file_kind', 'processing_status', 'id'),
        # Index for duplicate detection by size and checksum
        Index('idx_size_checksum', 'size_bytes', 'checksum', 'id'),
    )
    
    # Primary key: UUID v4
    id = Column(String(36), primary_key=True)  # Generated in application layer
    
    # File metadata
    original_name = Column(String(512), nullable=False)  # Original filename (e.g., "profile_photo.jpg")
    file_kind = Column(Enum(FileKindEnum), nullable=False)  # image or pdf
    storage_path = Column(String(768), nullable=False)  # Filesystem path (e.g., "/uploads/2024/11/abc123.jpg")
    mime_type = Column(String(128), nullable=False)  # e.g., "image/jpeg", "application/pdf"
    size_bytes = Column(BigInteger, nullable=False)  # File size in bytes
    checksum = Column(String(64), nullable=True)  # SHA256 hash (for integrity and duplicate detection)
    
    # Image-specific metadata (NULL for PDFs)
    width = Column(Integer, nullable=True)  # Image width in pixels
    height = Column(Integer, nullable=True)  # Image height in pixels
    
    # Generated assets
    thumbnail_path = Column(String(768), nullable=True)  # Thumbnail for images (e.g., "/thumbs/abc123_thumb.jpg")
    candidate_pdf_path = Column(String(768), nullable=True)  # Temporary PDF awaiting approval
    
    # Processing workflow
    processing_status = Column(
        Enum(ProcessingStatusEnum), 
        nullable=False, 
        default=ProcessingStatusEnum.pending
    )
    
    # Versioning (file revision history)
    version_of = Column(
        String(36), 
        ForeignKey('files.id', ondelete='SET NULL'), 
        nullable=True
    )  # References previous version of this file
    
    # Audit timestamps
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(
        DateTime, 
        nullable=False, 
        server_default=func.current_timestamp(), 
        onupdate=func.current_timestamp()
    )
