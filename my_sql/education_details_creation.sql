-- Use the target database
USE manamalai_db;
GO

-- Create the 'education_details' table
CREATE TABLE education_details (
    id INT PRIMARY KEY AUTO_INCREMENT,
    profile_id INT NOT NULL,
    degree VARCHAR(100),
    specialization VARCHAR(100),
    institution VARCHAR(200),
    location VARCHAR(100),
    year_of_completion INT,
    grade_percentage DECIMAL(5,2),
    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
);
GO