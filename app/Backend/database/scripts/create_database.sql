
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
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(15),
    company VARCHAR(255),
    role VARCHAR(100),
    score INT
);
ALTER TABLE customer AUTO_INCREMENT = 0;

CREATE TABLE IF NOT EXISTS employee (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT,
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
    Status ENUM('open', 'progress', 'closed', 'reopened') DEFAULT 'open',
    Priority ENUM('critical','high','medium', 'low') DEFAULT 'medium',
    Issue_Type ENUM('bug', 'error', 'issue', 'story', 'others', 'feature', 'enhancement', 'support') DEFAULT 'issue',
    Channel VARCHAR(100),
    Customer_ID INT,
    Product_ID VARCHAR(100),
    Medium VARCHAR(100),
    Team VARCHAR(50),
    Assignee_ID INT,
    Resolution TEXT,
    Issue_Date DATETIME DEFAULT CURRENT_TIMESTAMP,
    First_Response_Time DATETIME,
    Time_to_Resolution INT,
    Reopens INT DEFAULT 0,
    Story_Points INT,
    Score INT,
    FOREIGN KEY (Customer_ID) REFERENCES customer(id) ON DELETE SET NULL,
    FOREIGN KEY (Assignee_ID) REFERENCES employee(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS attachments(
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Ticket_Id INT,
    url TEXT,
    FOREIGN KEY (Ticket_Id) REFERENCES ticket(Ticket_Id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS comments (
    Ticket_id INT NOT NULL,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    Comment_user INT,
    Comment TEXT,
    FOREIGN KEY (Ticket_id) REFERENCES ticket(Ticket_Id) ON DELETE CASCADE  -- Added foreign key for ticket
);