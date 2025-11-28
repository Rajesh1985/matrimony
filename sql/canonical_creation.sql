CREATE TABLE files (
  id CHAR(36) NOT NULL PRIMARY KEY,               -- UUID v4 string
  owner_id BIGINT NOT NULL,                       -- references your users table
  original_name VARCHAR(512) NOT NULL,
  storage_type ENUM('local','s3') NOT NULL DEFAULT 'local',
  storage_path VARCHAR(1024) NOT NULL,            -- local filesystem path or s3 key
  candidate_pdf_path VARCHAR(1024) NULL,          -- temp generated PDF awaiting approval
  mime_type VARCHAR(128) NOT NULL,
  size_bytes BIGINT NOT NULL,
  checksum CHAR(64) NULL,                         -- sha256 hex
  width INT NULL,
  height INT NULL,
  thumbnail_path VARCHAR(1024) NULL,
  processing_status ENUM('pending','quarantined','scanning','ready','rejected') NOT NULL DEFAULT 'pending',
  encrypted TINYINT(1) NOT NULL DEFAULT 0,        -- 1 if file is encrypted on disk
  encryption_meta JSON NULL,                      -- { "method":"luks" } or envelope key info
  visibility ENUM('private','shared','public') NOT NULL DEFAULT 'private',
  storage_extra JSON NULL,                        -- reserved for future S3 metadata or headers
  version_of CHAR(36) NULL,                       -- points to previous file id if versioning kept
  created_by BIGINT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX(owner_id),
  INDEX(processing_status),
  INDEX(created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE user_photos (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT NOT NULL,
  file_id CHAR(36) NOT NULL,          -- FK to files.id
  position TINYINT NOT NULL,          -- 1..4 to represent ordered slots
  caption VARCHAR(255) NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY user_pos_unique (user_id, position),
  FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE profile_photos (
  user_id BIGINT NOT NULL PRIMARY KEY,
  file_id CHAR(36) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE horoscopes (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT NOT NULL,            -- owner
  file_id CHAR(36) NOT NULL,
  is_primary TINYINT(1) NOT NULL DEFAULT 1,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE government_ids (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT NOT NULL UNIQUE,     -- 1:1 with user for primary gov id; extendable for multiple types
  file_id CHAR(36) NOT NULL,
  id_type VARCHAR(64) NOT NULL,       -- e.g., "passport", "aadhar", "voter"
  masked_value VARCHAR(128) NULL,     -- for quick UI display without leaking full number
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE,
  INDEX(user_id),
  INDEX(id_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE community_certificates (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT NOT NULL UNIQUE,
  file_id CHAR(36) NOT NULL,
  certificate_type VARCHAR(128) NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE file_acl (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  file_id CHAR(36) NOT NULL,
  grantee_user_id BIGINT NOT NULL,       -- user who is granted access
  grantor_user_id BIGINT NOT NULL,       -- owner who granted access
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY file_grantee_unique (file_id, grantee_user_id),
  FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE file_processing_results (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  file_id CHAR(36) NOT NULL,
  ocr_text LONGTEXT NULL,
  ocr_lang VARCHAR(16) NULL,
  extracted_data JSON NULL,    -- structured fields extracted by OCR or rules
  processed_at TIMESTAMP NULL,
  worker_info VARCHAR(255) NULL,
  FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE,
  INDEX(processed_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE file_audit (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  file_id CHAR(36) NULL,
  user_id BIGINT NULL,
  action ENUM('upload','delete','download','share_grant','share_revoke','approve_conversion') NOT NULL,
  ip_address VARCHAR(45) NULL,
  details JSON NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX(file_id),
  INDEX(user_id),
  INDEX(created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

