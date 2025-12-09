-- Create new database
CREATE DATABASE IF NOT EXISTS manamalai_dev;

-- Use the new database
USE manamalai_dev;

-- Create the 'addresses' table in SQL Server
CREATE TABLE addresses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    profile_id INT NOT NULL,
    address_line1 VARCHAR(255),
    address_line2 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    postal_code VARCHAR(20),
    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
);
