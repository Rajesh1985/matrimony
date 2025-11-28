-- Create new database
CREATE DATABASE IF NOT EXISTS manamalai_dev;

-- Use the new database
USE manamalai_dev;

-- Create profiles table with adjusted column sizes
CREATE TABLE profiles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    serial_number VARCHAR(20) UNIQUE,
    name VARCHAR(100) NOT NULL,
    birth_date DATE,
    birth_time TIME,
    height_cm INT,
    complexion VARCHAR(50),
    caste VARCHAR(100) DEFAULT 'Vanniyar',
    mobile_number VARCHAR(20),
    introducer_name VARCHAR(100),
    introducer_mobile VARCHAR(20),
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    hobbies VARCHAR(500),
    about_me VARCHAR(2048),
    physical_status ENUM('Normal', 'Physically Challenged'),
    marital_status ENUM('Unmarried', 'Widow_Widower', 'Divorced', 'Separated'),
    food_preference ENUM('Veg', 'NonVeg'),
    religion VARCHAR(50) DEFAULT 'hindu',

    address_line1 VARCHAR(255),
    address_line2 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    postal_code VARCHAR(20),

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1
);

-- Drop existing trigger, if any
DROP TRIGGER IF EXISTS trg_generate_serial_number;

-- Trigger for serial number generation
DELIMITER //
CREATE TRIGGER trg_generate_serial_number
BEFORE INSERT ON profiles
FOR EACH ROW
BEGIN
    SET NEW.serial_number = CONCAT(
        'CVM',
        RIGHT(CONCAT('00000000000', CAST(NEW.id AS CHAR)), 11)
    );
END;
//
DELIMITER ;
