CREATE DATABASE IF NOT EXISTS nullbyte;
USE nullbyte;

CREATE TABLE IF NOT EXISTS customer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(15) NOT NULL,
    company VARCHAR(255),
    role VARCHAR(100),
    score INT
);

CREATE TABLE IF NOT EXISTS employee (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(15) NOT NULL,
    role VARCHAR(100),
    score INT,
    Manager INT,
    GCM VARCHAR(100),
    Experience INT,
    FOREIGN KEY (Manager) REFERENCES employee(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS ticket (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Subject VARCHAR(255) NOT NULL,
    Type VARCHAR(100),
    Description TEXT NOT NULL,
    Status ENUM('Open', 'In Progress', 'Closed', 'Reopened') NOT NULL,
    Priority ENUM('Low', 'Medium', 'High') NOT NULL,
    Channel VARCHAR(100),
    Customer_ID INT,
    Product_ID INT,
    Employee_ID INT,
    Resolution TEXT,
    Issue_Date DATETIME DEFAULT CURRENT_TIMESTAMP,
    First_Response_Time DATETIME,
    Time_to_Resolution INT,
    Reopens INT DEFAULT 0,
    Score INT,
    FOREIGN KEY (Customer_ID) REFERENCES customer(id) ON DELETE CASCADE,
    FOREIGN KEY (Employee_ID) REFERENCES employee(id) ON DELETE SET NULL
);