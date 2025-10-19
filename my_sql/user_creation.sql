USE manamalai_db;
GO

DROP TABLE Users;

-- Create the 'Users' table in SQL Server
CREATE TABLE Users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    country_code VARCHAR(5) NOT NULL,
    name VARCHAR(100) NOT NULL,
    mobile VARCHAR(15) UNIQUE,
    email_id VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    profile_id INT,
    is_verified BOOLEAN DEFAULT 0,
    otp_code VARCHAR(6),
    otp_created_at DATETIME,
    gender VARCHAR(10),
    CHECK (gender IN ('Male', 'Female', 'Other'))
);
GO