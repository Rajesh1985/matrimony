USE [manamalai]
GO

-- Create the 'astrology_details' table in SQL Server
CREATE TABLE astrology_details (
    id INT PRIMARY KEY IDENTITY(1,1),
    profile_id INT NOT NULL,
    star VARCHAR(50),
    rasi VARCHAR(50), 
    lagnam VARCHAR(50), 
    birth_place VARCHAR(100),
    gotram VARCHAR(50),
    dosham_details VARCHAR(MAX),
    horoscope_url VARCHAR(255), -- Link to horoscope document
    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
);
GO