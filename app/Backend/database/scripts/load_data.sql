
USE nullbyte;
LOAD DATA INFILE '/mnt/c/Users/Jesvi Jonathan/Desktop/Nullbyte-Ticketing-System/app/Backend/database/data/customer_table.csv'
INTO TABLE customer
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS
(name, age, gender, email, phone, company, role, score);

LOAD DATA INFILE '/mnt/c/Users/Jesvi Jonathan/Desktop/Nullbyte-Ticketing-System/app/Backend/database/data/employee_table.csv'
INTO TABLE employee
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS
(name, age, gender, email, phone, role, score, @manager, gcm, experience);