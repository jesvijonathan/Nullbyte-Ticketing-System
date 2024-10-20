
USE nullbyte;
LOAD DATA INFILE '/var/lib/mysql-files/customer_table.csv'
INTO TABLE customer
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS
(name, age, gender, username, password, email, phone, company, role, score);

LOAD DATA INFILE '/var/lib/mysql-files/employee_table.csv'
INTO TABLE employee
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS
(name, age, gender, username, password, email, phone, role, score, @manager, gcm, experience)
SET manager = NULLIF(@manager, '');

-- LOAD DATA INFILE '/var/lib/mysql-files/ticket_table.csv'
-- INTO TABLE ticket
-- FIELDS TERMINATED BY ',' 
-- ENCLOSED BY '"' 
-- LINES TERMINATED BY '\n' 
-- IGNORE 1 ROWS
-- (Chat_Id, Subject, Summary, Analysis, Type, Description, Status, Priority, Issue_Type, Channel, Customer_ID, Product_TYPE, Medium, Team, @Assignee_ID, Resolution, @Issue_Date, Reopens, @Story_Points, @Score)
-- SET Assignee_ID = NULLIF(@Assignee_ID, ''),
--     Issue_Date = STR_TO_DATE(@Issue_Date, '%Y-%m-%d %H:%i:%s'),
--     Reopens = NULLIF(Reopens, ''),
--     Score = NULLIF(NULLIF(@Score, ''), '0'),
--     Story_Points = NULLIF(@Story_Points, '');


-- LOAD DATA INFILE '/var/lib/mysql-files/attachments_table.csv'
-- INTO TABLE attachments
-- FIELDS TERMINATED BY ',' 
-- ENCLOSED BY '"' 
-- LINES TERMINATED BY '\n' 
-- IGNORE 1 ROWS
-- (Id, Ticket_Id, url);