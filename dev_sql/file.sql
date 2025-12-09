-- Create new database
CREATE DATABASE IF NOT EXISTS manamalai_dev;

-- Use the new database
USE manamalai_dev;

-- Create the 'files' table in SQL Server
CREATE TABLE files (
  id CHAR(36) NOT NULL PRIMARY KEY,                                 -- UUID v4 string
  original_name VARCHAR(512) NOT NULL,
  file_kind ENUM('image','pdf') NOT NULL,                           -- logical kind for fast filtering
  storage_path VARCHAR(768) NOT NULL,                               -- filesystem path
  mime_type VARCHAR(128) NOT NULL,                                  -- standardized file type
  size_bytes BIGINT UNSIGNED NOT NULL,
  checksum CHAR(64) NULL,                                           -- sha256 hex
  width INT UNSIGNED NULL,                                          -- only for images
  height INT UNSIGNED NULL,                                         -- only for images
  thumbnail_path VARCHAR(768) NULL,                                 -- generated thumbnail for images
  candidate_pdf_path VARCHAR(768) NULL,                             -- temporary generated PDF awaiting approval
  processing_status ENUM('pending','quarantined','scanning','ready','rejected') NOT NULL DEFAULT 'pending',
  version_of CHAR(36) NULL,                                         -- previous file id (if versioning)
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_files_version_of FOREIGN KEY (version_of) REFERENCES files(id) ON DELETE SET NULL,
  CONSTRAINT chk_filekind_mime CHECK (
    (file_kind = 'image' AND mime_type LIKE 'image/%')
    OR (file_kind = 'pdf' AND mime_type = 'application/pdf')
  ),
  INDEX idx_filekind_status (file_kind, processing_status, id),
  INDEX idx_size_checksum (size_bytes, checksum, id)
);