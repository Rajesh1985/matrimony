-- Create new database
CREATE DATABASE IF NOT EXISTS manamalai_dev;

-- Use the new database
USE manamalai_dev;

-- Create the 'addresses' table in SQL Server
CREATE TABLE partner_preferences (
    id INT PRIMARY KEY AUTO_INCREMENT,
    profile_id INT NOT NULL,
    age_from INT,
    age_to INT,
    height_from INT, -- in cm
    height_to INT,   -- in cm
    education_preference TEXT,
    occupation_preference TEXT,
    income_preference TEXT,
    star_preference TEXT, -- Comma-separated list of preferred stars
    rasi_preference TEXT, -- Comma-separated list of preferred rasis
    location_preference TEXT,
    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
);
