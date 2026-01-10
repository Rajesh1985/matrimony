# app/utils/file_handler.py
"""
File handling utilities for photo upload and processing
- Virus scanning
- Image conversion
- Checksum calculation
- File validation
"""

import hashlib
import os
import subprocess
from pathlib import Path
from typing import Tuple, Optional
from PIL import Image
import io
import uuid


# ==================== FILE VALIDATION ====================

def validate_file_size(file_content: bytes, max_size_mb: int = 10) -> Tuple[bool, Optional[str]]:
    """
    Validate file size
    
    Args:
        file_content: File bytes
        max_size_mb: Maximum allowed size in MB
    
    Returns:
        Tuple[is_valid, error_message]
    """
    max_bytes = max_size_mb * 1024 * 1024
    if len(file_content) > max_bytes:
        print(f"File size {len(file_content)} exceeds max allowed {max_bytes}")
        return False, "SIZE_EXCEEDED"
    return True, None


def validate_mime_type(mime_type: str, allowed_types: list = None) -> Tuple[bool, Optional[str]]:
    """
    Validate file MIME type
    
    Args:
        mime_type: File MIME type
        allowed_types: List of allowed MIME types (default: image types)
    
    Returns:
        Tuple[is_valid, error_message]
    """
    if allowed_types is None:
        allowed_types = [
            'image/jpeg',
            'image/jpg',
            'image/png',
            'image/webp',
            'image/gif'
        ]
    
    if mime_type not in allowed_types:
        return False, "INVALID_FILE_TYPE"
    return True, None


# ==================== CHECKSUM & DUPLICATE DETECTION ====================

def calculate_checksum(file_content: bytes) -> str:
    """
    Calculate SHA256 checksum of file content
    
    Args:
        file_content: File bytes
    
    Returns:
        SHA256 hex string
    """
    return hashlib.sha256(file_content).hexdigest()


# ==================== VIRUS SCANNING ====================

def scan_file_with_clamav(file_path: str) -> Tuple[bool, Optional[str]]:
    """
    Scan file for viruses using ClamAV
    
    Args:
        file_path: Path to file to scan
    
    Returns:
        Tuple[is_safe, error_message]
        is_safe: True if no virus found, False if virus detected
    """
    try:
        # Try using clamdscan (daemon mode, faster)
        result = subprocess.run(
            ['clamdscan', '--no-summary', '--remove', file_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            # File is clean
            return True, None
        elif result.returncode == 1:
            # Virus found
            return False, "VIRUS_FOUND"
        else:
            # Scanning error
            return False, "SCANNING_ERROR"
            
    except FileNotFoundError:
        # ClamAV not installed, try clamscan instead
        try:
            result = subprocess.run(
                ['clamscan', '--no-summary', '--remove', file_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return True, None
            elif result.returncode == 1:
                return False, "VIRUS_FOUND"
            else:
                return False, "SCANNING_ERROR"
                
        except FileNotFoundError:
            # ClamAV not available, skip scanning with warning
            print("WARNING: ClamAV not installed, skipping virus scan")
            return True, None
        except subprocess.TimeoutExpired:
            # Scan timed out
            return False, "SCAN_TIMEOUT"
    except subprocess.TimeoutExpired:
        return False, "SCAN_TIMEOUT"
    except Exception as e:
        print(f"Error during virus scan: {e}")
        # Don't block upload if scanning fails
        return True, None


# ==================== IMAGE CONVERSION ====================

def convert_to_webp(file_content: bytes, quality: int = 85) -> Tuple[bytes, Optional[str]]:
    """
    Convert image to WebP format, preserving EXIF data
    
    Args:
        file_content: Original image bytes
        quality: WebP quality (1-100, default 85)
    
    Returns:
        Tuple[webp_bytes, error_message]
    """
    try:
        # Open image from bytes
        img = Image.open(io.BytesIO(file_content))
        
        # Preserve EXIF data if available
        exif_data = None
        try:
            exif_data = img.info.get('exif')
        except Exception:
            # EXIF data may not be present in all images; continue without it
            pass

        # Convert to RGB if necessary (for RGBA images)
        if img.mode in ('RGBA', 'LA', 'P'):
            # Create white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Save as WebP
        webp_buffer = io.BytesIO()
        kwargs = {
            'format': 'WebP',
            'quality': quality,
            'method': 6  # Slow but better compression
        }
        
        # Add EXIF if available
        if exif_data:
            kwargs['exif'] = exif_data
        
        img.save(webp_buffer, **kwargs)
        webp_buffer.seek(0)
        
        return webp_buffer.getvalue(), None
        
    except Exception as e:
        print(f"Error converting image to WebP: {e}")
        return None, "CONVERSION_ERROR"


def generate_thumbnail(file_content: bytes, size: Tuple[int, int] = (150, 150)) -> Tuple[bytes, Optional[str]]:
    """
    Generate thumbnail from image
    
    Args:
        file_content: Image bytes
        size: Thumbnail size (width, height)
    
    Returns:
        Tuple[thumbnail_bytes, error_message]
    """
    try:
        img = Image.open(io.BytesIO(file_content))
        
        # Convert to RGB if necessary
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Create thumbnail
        img.thumbnail(size, Image.Resampling.LANCZOS)
        
        # Save as WebP
        thumb_buffer = io.BytesIO()
        img.save(thumb_buffer, format='WebP', quality=80)
        thumb_buffer.seek(0)
        
        return thumb_buffer.getvalue(), None
        
    except Exception as e:
        print(f"Error generating thumbnail: {e}")
        return None, "THUMBNAIL_ERROR"


# ==================== FILE STORAGE ====================

def ensure_directory(directory_path: str) -> bool:
    """
    Ensure directory exists, create if missing
    
    Args:
        directory_path: Path to directory
    
    Returns:
        True if successful, False if error
    """
    try:
        Path(directory_path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating directory {directory_path}: {e}")
        return False


def save_file_to_disk(file_content: bytes, file_path: str) -> Tuple[bool, Optional[str]]:
    """
    Save file content to disk
    
    Args:
        file_content: File bytes
        file_path: Path to save file to
    
    Returns:
        Tuple[success, error_message]
    """
    try:
        # Ensure directory exists
        directory = str(Path(file_path).parent)
        if not ensure_directory(directory):
            return False, "DIRECTORY_ERROR"
        
        # Write file
        with open(file_path, 'wb') as f:
            f.write(file_content)
        
        return True, None
        
    except Exception as e:
        print(f"Error saving file: {e}")
        return False, "SAVE_ERROR"


def delete_file_from_disk(file_path: str) -> Tuple[bool, Optional[str]]:
    """
    Delete file from disk
    
    Args:
        file_path: Path to file
    
    Returns:
        Tuple[success, error_message]
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
        return True, None
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False, "DELETE_ERROR"


# ==================== PATH GENERATION ====================

def generate_photo_filename(serial_number: str, slot_number: int, extension: str = ".webp") -> str:
    """
    Generate standardized photo filename
    
    Args:
        serial_number: User's profile serial number
        slot_number: Photo slot (1 or 2)
        extension: File extension
    
    Returns:
        Filename in format: {serial_number}_photo_{slot_number}.webp
    """
    return f"{serial_number}_photo_{slot_number}{extension}"


def generate_photo_path(serial_number: str, slot_number: int, base_dir: str = "./photos") -> str:
    """
    Generate full photo storage path
    
    Args:
        serial_number: User's profile serial number
        slot_number: Photo slot (1 or 2)
        base_dir: Base photo directory
    
    Returns:
        Full path to photo file
    """
    filename = generate_photo_filename(serial_number, slot_number)
    return os.path.join(base_dir, filename)


def generate_thumbnail_path(serial_number: str, slot_number: int, base_dir: str = "./thumbnails") -> str:
    """
    Generate full thumbnail storage path
    
    Args:
        serial_number: User's profile serial number
        slot_number: Photo slot (1 or 2)
        base_dir: Base thumbnail directory
    
    Returns:
        Full path to thumbnail file
    """
    filename = generate_photo_filename(serial_number, slot_number, ".webp")
    return os.path.join(base_dir, filename)


def generate_file_id() -> str:
    """
    Generate UUID for file
    
    Returns:
        UUID v4 string
    """
    return str(uuid.uuid4())


# ==================== PDF CONVERSION ====================

def image_to_pdf(image_bytes: bytes, mime_type: str = "image/jpeg") -> Tuple[Optional[bytes], Optional[str]]:
    """
    Convert image to PDF
    
    Args:
        image_bytes: Image file bytes
        mime_type: MIME type of image
    
    Returns:
        Tuple[pdf_bytes, error_message]
        - (pdf_bytes, None) if successful
        - (None, error_msg) if failed
    
    Purpose: Convert uploaded images (JPEG, PNG) to PDF for community certificates
    Preserves image quality and dimensions
    """
    try:
        # Open image from bytes
        img = Image.open(io.BytesIO(image_bytes))
        
        # Convert RGBA to RGB if needed (PDF doesn't support transparency)
        if img.mode == 'RGBA':
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[3])  # Use alpha channel as mask
            img = rgb_img
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Convert to PDF
        pdf_bytes = io.BytesIO()
        img.save(pdf_bytes, format='PDF', quality=95)
        return pdf_bytes.getvalue(), None
    
    except Exception as e:
        error_msg = f"Image to PDF conversion failed: {str(e)}"
        print(f"[PDF CONVERSION ERROR] {error_msg}")
        return None, error_msg


def validate_pdf_file(file_content: bytes) -> Tuple[bool, Optional[str]]:
    """
    Validate PDF file
    
    Args:
        file_content: File bytes
    
    Returns:
        Tuple[is_valid, error_message]
    """
    try:
        # Check PDF header
        if not file_content.startswith(b'%PDF-'):
            return False, "INVALID_PDF_FORMAT"
        return True, None
    except Exception as e:
        return False, f"PDF validation error: {str(e)}"
