USE manamalai_db;
GO
-- Create the 'addresses' table in SQL Server
CREATE TABLE addresses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    profile_id INT NOT NULL,
    address_type VARCHAR(20) NOT NULL,
    address_line1 VARCHAR(255),
    address_line2 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    postal_code VARCHAR(20),
    is_primary BOOLEAN DEFAULT 0,
    CHECK (address_type IN ('permanent', 'current', 'office', 'other')),
    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
);
GO