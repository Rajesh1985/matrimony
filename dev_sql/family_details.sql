-- Create new database
CREATE DATABASE IF NOT EXISTS manamalai_dev;

-- Use the new database
USE manamalai_dev;

-- family_details table (modified)
CREATE TABLE family_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    profile_id INT NOT NULL,
    father_name VARCHAR(100),
    father_occupation VARCHAR(100),
    mother_name VARCHAR(100),
    mother_occupation VARCHAR(100),
    brothers INT DEFAULT 0,
    sisters INT DEFAULT 0,
    Married_brothers INT DEFAULT 0,
    Married_sisters INT DEFAULT 0,
    family_type VARCHAR(20) DEFAULT 'nuclear',
    family_status ENUM('Middle_Class','upper_middle_class','Rich/Elite'),
    Family_description TEXT,
    CHECK (family_type IN ('nuclear', 'joint', 'extended')),
    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
);