-- Use the target database
USE [manamalai];
GO

-- Create the 'partner_preferences' table
CREATE TABLE partner_preferences (
    id INT PRIMARY KEY IDENTITY(1,1),
    profile_id INT NOT NULL,
    age_from INT,
    age_to INT,
    height_from INT, -- in cm
    height_to INT, -- in cm
    education_preference VARCHAR(MAX),
    occupation_preference VARCHAR(MAX),
    income_preference VARCHAR(MAX),
    caste_preference VARCHAR(MAX),
    star_preference VARCHAR(MAX), -- Comma-separated list of preferred stars
    rasi_preference VARCHAR(MAX), -- Comma-separated list of preferred rasis
    location_preference VARCHAR(MAX),
    other_preferences VARCHAR(MAX),
    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
);
GO