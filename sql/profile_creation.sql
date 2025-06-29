USE [manamalai]
GO

-- Create the 'profiles' table
CREATE TABLE profiles (
    id INT PRIMARY KEY IDENTITY(1,1),
    serial_number VARCHAR(20) UNIQUE,
    name VARCHAR(100) NOT NULL,
    birth_date DATE,
    birth_time TIME,
    height_cm INT, 
    complexion VARCHAR(50), 
    caste VARCHAR(100), 
    sub_caste VARCHAR(100), 
    mobile_number VARCHAR(20),
    introducer_name VARCHAR(100),
    introducer_mobile VARCHAR(20),
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE(),
    is_active BIT DEFAULT 1
);
GO

-- Trigger to generate the serial_number after insert
CREATE TRIGGER trg_generate_serial_number
ON profiles
AFTER INSERT
AS
BEGIN
    UPDATE p
    SET serial_number = 'CVM' + RIGHT('00000000000' + CAST(p.id AS VARCHAR), 11)
    FROM profiles p
    INNER JOIN inserted i ON p.id = i.id;
END;
GO

-- Trigger to update the updated_at timestamp on record update
CREATE TRIGGER trg_profiles_update_timestamp
ON profiles
AFTER UPDATE
AS
BEGIN
    UPDATE p
    SET updated_at = GETDATE()
    FROM profiles p
    INNER JOIN inserted i ON p.id = i.id;
END;
GO