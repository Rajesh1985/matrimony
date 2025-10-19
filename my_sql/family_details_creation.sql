USE manamalai_db;
GO

-- Create the 'family_details' table in SQL Server
CREATE TABLE family_details (
    id INT PRIMARY KEY AUTO_INCREMENT,
    profile_id INT NOT NULL,
    father_name VARCHAR(100),
    father_occupation VARCHAR(100),
    mother_name VARCHAR(100),
    mother_occupation VARCHAR(100),
    total_siblings INT DEFAULT 0,
    married_siblings INT DEFAULT 0,
    family_type VARCHAR(20) DEFAULT 'nuclear',
    family_status VARCHAR(100),
    family_values TEXT,
    CHECK (family_type IN ('nuclear', 'joint', 'extended')),
    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
);
GO