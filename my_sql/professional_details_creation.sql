-- Use the target database
USE manamalai_db;
GO

-- Create the 'professional_details' table
CREATE TABLE professional_details (
    id INT PRIMARY KEY AUTO_INCREMENT,
    profile_id INT NOT NULL,
    designation VARCHAR(100),
    company_name VARCHAR(200),
    industry VARCHAR(100),
    experience_years DECIMAL(4,1),
    monthly_income DECIMAL(12,2),
    annual_income DECIMAL(12,2),
    work_location VARCHAR(100),
    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
);
GO