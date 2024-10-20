
-- CREATE TABLE Customer (
--     CustomerID INT IDENTITY(1,1) PRIMARY KEY,
--     FirstName NVARCHAR(50) NOT NULL,
--     LastName NVARCHAR(50) NOT NULL,
--     Email NVARCHAR(100) NOT NULL UNIQUE,
--     PhoneNumber NVARCHAR(15) NOT NULL,
--     Address NVARCHAR(255),
--     Username NVARCHAR(50) NOT NULL UNIQUE,
--     Password NVARCHAR(255) NOT NULL,
--     RegistrationDate DATETIME DEFAULT GETDATE()
-- );

-- CREATE TABLE Vehicle (
--     VehicleID INT PRIMARY KEY IDENTITY(1,1),
--     Model VARCHAR(100),
--     Make VARCHAR(100),
--     Year INT,
--     Color VARCHAR(50),
--     RegistrationNumber VARCHAR(100) UNIQUE,
--     Availability VARCHAR(5) CHECK (Availability IN ('yes', 'no')),
--     DailyRate DECIMAL(10, 2)
-- );

-- CREATE TABLE Reservation (
--     ReservationID INT IDENTITY(1,1) PRIMARY KEY, 
--     CustomerID INT NOT NULL, 
--     VehicleID INT NOT NULL, 
--     StartDate DATE NOT NULL,  
--     EndDate DATE NOT NULL, 
--     TotalCost DECIMAL(10, 2) NOT NULL,  
--     Status NVARCHAR(20) NOT NULL CHECK (Status IN ('pending', 'confirmed', 'completed')), 
--     FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
--     FOREIGN KEY (VehicleID) REFERENCES Vehicle(VehicleID)
-- );

-- CREATE TABLE Admin (
--     AdminID INT IDENTITY(1,1) PRIMARY KEY, 
--     FirstName NVARCHAR(50) NOT NULL,
--     LastName NVARCHAR(50) NOT NULL,
--     Email NVARCHAR(50) NOT NULL UNIQUE,   
--     PhoneNumber INT NOT NULL,     
--     Username NVARCHAR(50) NOT NULL UNIQUE,  
--     Password NVARCHAR(50) NOT NULL,     
--     Role NVARCHAR(20) NOT NULL CHECK (Role IN ('Super admin', 'fleet manager')),             
--     JoinDate DATE NOT NULL DEFAULT GETDATE()
-- );

-- select * from Customer
select * from Vehicle
select * from Admin
select * from Reservation







