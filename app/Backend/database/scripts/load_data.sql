
USE nullbyte;
LOAD DATA INFILE '/var/lib/mysql-files/customer_table.csv'
INTO TABLE customer
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS
(name, age, gender, email, phone, company, role, score);

LOAD DATA INFILE '/var/lib/mysql-files/employee_table.csv'
INTO TABLE employee
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS
(name, age, gender, email, phone, role, score, @manager, gcm, experience);

LOAD DATA INFILE '/var/lib/mysql-files/ticket_table.csv'
INTO TABLE ticket
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS
(Ticket_Id, Chat_Id, Subject, Summary, Analysis, Type, Description, Status, Priority, Issue_Type, Channel, Customer_ID, Product_ID, Medium, Team, @Assignee_ID, Resolution, Issue_Date, @First_Response_Time, @Time_to_Resolution, Reopens, @Story_Points, @Score)
SET Assignee_ID = NULLIF(@Assignee_ID, ''),
    First_Response_Time = NULLIF(@First_Response_Time, ''),
    Time_to_Resolution = NULLIF(@Time_to_Resolution, ''),
    Score = Score = NULLIF(NULLIF(@Score, ''), '0'),
    Story_Points = NULLIF(@Story_Points, '');

LOAD DATA INFILE '/var/lib/mysql-files/attachments_table.csv'
INTO TABLE attachments
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS
(Id, Ticket_Id, url);