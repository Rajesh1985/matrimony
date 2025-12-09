-- Create new database
CREATE DATABASE IF NOT EXISTS manamalai_dev;

-- Use the new database
USE manamalai_dev;

-- Create the 'professional_details' table in SQL Server
CREATE TABLE professional_details (
    id INT PRIMARY KEY AUTO_INCREMENT,
    profile_id INT NOT NULL,
    education VARCHAR(100),
    education_optional VARCHAR(100),
    employment_type VARCHAR(100),
    occupation VARCHAR(100),
    company_name VARCHAR(200),
    annual_income VARCHAR(100),
    work_location VARCHAR(100),
    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
);