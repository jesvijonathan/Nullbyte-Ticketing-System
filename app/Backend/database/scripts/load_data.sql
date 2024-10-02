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