USE manamalai_db;
GO

-- Create the 'astrology_details' table in SQL Server
CREATE TABLE astrology_details (
    id INT PRIMARY KEY AUTO_INCREMENT,
    profile_id INT NOT NULL,
    star VARCHAR(50),
    rasi VARCHAR(50),
    lagnam VARCHAR(50),
    birth_place VARCHAR(100),
    gotram VARCHAR(50),
    dosham_details TEXT,
    horoscope_url VARCHAR(255),
    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
);
GO