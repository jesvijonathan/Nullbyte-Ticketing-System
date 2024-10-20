
CREATE DATABASE IF NOT EXISTS nullbyte;
USE nullbyte;

CREATE USER IF NOT EXISTS 'nullbyteadmin'@'%' IDENTIFIED BY 'rootpassword';
GRANT ALL PRIVILEGES ON nullbyte.* TO 'nullbyteadmin'@'%';
FLUSH PRIVILEGES;

CREATE TABLE IF NOT EXISTS customer (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT,
    gender ENUM('Male', 'Female'),
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(15),
    company VARCHAR(255),
    role VARCHAR(100),
    score INT
);
ALTER TABLE customer AUTO_INCREMENT = 0;

CREATE TABLE IF NOT EXISTS employee (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    gender ENUM('Male', 'Female') NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(15),
    role VARCHAR(100),
    score INT,
    manager INT DEFAULT NULL,
    gcm INT,
    experience INT,
    FOREIGN KEY (manager) REFERENCES employee(id) ON DELETE SET NULL
);
ALTER TABLE employee AUTO_INCREMENT = 0;
CREATE TABLE IF NOT EXISTS ticket (
    Ticket_Id INT AUTO_INCREMENT PRIMARY KEY,
    Chat_Id VARCHAR(50),
    Subject VARCHAR(255) NOT NULL,
    Summary TEXT NOT NULL,
    Analysis TEXT,
    Type VARCHAR(100),
    Description TEXT,
    Status ENUM('open', 'progress', 'closed', 'reopened','waiting for information') DEFAULT 'open',
    Priority ENUM('critical','high','medium', 'low') DEFAULT 'medium',
    Issue_Type ENUM('bug', 'error', 'issue', 'story', 'others', 'feature', 'enhancement', 'support','task') DEFAULT 'issue',
    Channel VARCHAR(100),
    Customer_ID INT,
    Product_Type VARCHAR(100),
    Medium VARCHAR(100),
    Team VARCHAR(50),
    Assignee_ID INT,
    Resolution TEXT,
    Issue_Date DATETIME DEFAULT CURRENT_TIMESTAMP,
    Created DATETIME,
    LastModified DATETIME,
    Estimation INT,
    Reopens INT DEFAULT 0,
    Story_Points INT,
    Score INT,
    FOREIGN KEY (Customer_ID) REFERENCES customer(id) ON DELETE SET NULL,
    FOREIGN KEY (Assignee_ID) REFERENCES employee(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS attachments(
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Ticket_Id INT,
    Name VARCHAR(100),
    Type VARCHAR(50),
    Size VARCHAR(10),
    Url TEXT,
    FOREIGN KEY (Ticket_Id) REFERENCES ticket(Ticket_Id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS comments (
    Ticket_id INT NOT NULL,
    Comment_id INT AUTO_INCREMENT PRIMARY KEY,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    Comment_user INT,
    Comment TEXT,
    FOREIGN KEY (Ticket_id) REFERENCES ticket(Ticket_Id) ON DELETE CASCADE  
);

-- CREATE TABLE IF NOT EXIST worklog (
--     Id INT AUTO_INCREMENT PRIMARY KEY,
--     Ticket_Id INT,
--     Worklog_User INT,
--     Worklog_Date DATETIME DEFAULT CURRENT_TIMESTAMP,
--     Worklog_Hours INT,
--     Worklog TEXT,
--     FOREIGN KEY (Ticket_Id) REFERENCES ticket(Ticket_Id) ON DELETE CASCADE
--     FOREIGN KEY (Worklog_User) REFERENCES employee(id) ON DELETE SET NULL
-- );
CREATE TABLE IF NOT EXISTS worklog (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Ticket_Id INT,
    Worklog_User INT,
    Worklog_Date DATETIME DEFAULT CURRENT_TIMESTAMP,
    Worklog_Hours INT,
    Worklog TEXT,
    FOREIGN KEY (Ticket_Id) REFERENCES ticket(Ticket_Id) ON DELETE CASCADE,
    FOREIGN KEY (Worklog_User) REFERENCES employee(id) ON DELETE SET NULL
);