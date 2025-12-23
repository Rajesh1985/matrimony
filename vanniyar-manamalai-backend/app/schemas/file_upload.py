# app/schemas/file_upload.py
"""
File upload schemas for photo upload endpoint
Handles request/response validation for profile photo uploads
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class ErrorCodeEnum(str, Enum):
    """Error codes for file upload failures"""
    SIZE_EXCEEDED = "SIZE_EXCEEDED"
    VIRUS_FOUND = "VIRUS_FOUND"
    DUPLICATE_DETECTED = "DUPLICATE_DETECTED"
    NO_FREE_SLOT = "NO_FREE_SLOT"
    INVALID_FILE_TYPE = "INVALID_FILE_TYPE"
    PROCESSING_ERROR = "PROCESSING_ERROR"
    NOT_FOUND = "NOT_FOUND"
    UNAUTHORIZED = "UNAUTHORIZED"


class FileUploadResponse(BaseModel):
    """Successful file upload response"""
    status: str = "success"
    file_id: str
    thumbnail_url: str
    profile_id: Optional[int] = None
    original_name: Optional[str] = None
    mime_type: Optional[str] = None
    size_bytes: Optional[int] = None
    processing_status: str = "ready"

    class Config:
        from_attributes = True


class FileUploadErrorResponse(BaseModel):
    """Failed file upload response"""
    status: str = "error"
    code: ErrorCodeEnum
    message: str
    file_name: Optional[str] = None


class FileDeleteResponse(BaseModel):
    """File deletion response"""
    status: str = "success"
    message: str
    file_id: str
    deleted_at: Optional[str] = None


class FileDeleteErrorResponse(BaseModel):
    """File deletion error response"""
    status: str = "error"
    code: ErrorCodeEnum
    message: str


class FileMetadataResponse(BaseModel):
    """File metadata response"""
    file_id: str
    original_name: str
    mime_type: str
    size_bytes: int
    processing_status: str
    created_at: Optional[str] = None

    class Config:
        from_attributes = True
