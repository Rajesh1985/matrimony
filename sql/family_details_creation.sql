USE [manamalai]
GO

-- Create the 'family_details' table in SQL Server
CREATE TABLE family_details (
    id INT PRIMARY KEY IDENTITY(1,1),
    profile_id INT NOT NULL,
    father_name VARCHAR(100),
    father_occupation VARCHAR(100),
    mother_name VARCHAR(100),
    mother_occupation VARCHAR(100),
    total_siblings INT DEFAULT 0,
    married_siblings INT DEFAULT 0,
    family_type VARCHAR(20) DEFAULT 'nuclear' CHECK (family_type IN ('nuclear', 'joint', 'extended')),
    family_status VARCHAR(100),
    family_values VARCHAR(MAX),
    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
);
GO