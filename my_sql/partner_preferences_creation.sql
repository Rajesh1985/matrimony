-- Use the target database
USE manamalai_db;
GO

-- Create the 'partner_preferences' table
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
    caste_preference TEXT,
    star_preference TEXT, -- Comma-separated list of preferred stars
    rasi_preference TEXT, -- Comma-separated list of preferred rasis
    location_preference TEXT,
    other_preferences TEXT,
    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
);
GO