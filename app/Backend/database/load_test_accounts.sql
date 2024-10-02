USE nullbyte;

INSERT INTO customer (name, age, gender, email, phone, company, role, score) VALUES
('Alice Johnson', 30, 'Female', 'alice.johnson@example.com', '1234567890', 'Tech Corp', 'Customer', 85),
('Bob Smith', 28, 'Male', 'bob.smith@example.com', '1234567891', 'Innovate LLC', 'Customer', 90),
('Charlie Brown', 35, 'Male', 'charlie.brown@example.com', '1234567892', 'NextGen Inc', 'Customer', 78),
('Daisy White', 22, 'Female', 'daisy.white@example.com', '1234567893', 'Future Solutions', 'Customer', 88),
('Ethan Hunt', 40, 'Male', 'ethan.hunt@example.com', '1234567894', 'Prime Services', 'Customer', 95),
('Fiona Green', 29, 'Female', 'fiona.green@example.com', '1234567895', 'Global Enterprises', 'Customer', 80),
('George Black', 45, 'Male', 'george.black@example.com', '1234567896', 'Visionary Tech', 'Customer', 70),
('Hannah Brown', 33, 'Female', 'hannah.brown@example.com', '1234567897', 'Smart Solutions', 'Customer', 82),
('Ian Wright', 27, 'Male', 'ian.wright@example.com', '1234567898', 'Dynamic Industries', 'Customer', 87),
('Julia Roberts', 31, 'Female', 'julia.roberts@example.com', '1234567899', 'Innovation Hub', 'Customer', 92);

INSERT INTO employee (name, age, gender, email, phone, role, score, Manager, GCM, Experience) VALUES
('Alice Johnson', 30, 'Female', 'alice.johnson.emp@example.com', '1234567890', 'Sales', 85, NULL, 'GCM1', 5),
('Bob Smith', 28, 'Male', 'bob.smith.emp@example.com', '1234567891', 'Support', 90, 1, 'GCM2', 3),
('Charlie Brown', 35, 'Male', 'charlie.brown.emp@example.com', '1234567892', 'Development', 78, 1, 'GCM3', 8),
('Daisy White', 22, 'Female', 'daisy.white.emp@example.com', '1234567893', 'HR', 88, NULL, 'GCM4', 2),
('Ethan Hunt', 40, 'Male', 'ethan.hunt.emp@example.com', '1234567894', 'Management', 95, 3, 'GCM5', 10),
('Fiona Green', 29, 'Female', 'fiona.green.emp@example.com', '1234567895', 'Marketing', 80, 2, 'GCM6', 4),
('George Black', 45, 'Male', 'george.black.emp@example.com', '1234567896', 'Finance', 70, 5, 'GCM7', 12),
('Hannah Brown', 33, 'Female', 'hannah.brown.emp@example.com', '1234567897', 'Development', 82, 3, 'GCM8', 7),
('Ian Wright', 27, 'Male', 'ian.wright.emp@example.com', '1234567898', 'Support', 87, 4, 'GCM9', 3),
('Julia Roberts', 31, 'Female', 'julia.roberts.emp@example.com', '1234567899', 'Sales', 92, 5, 'GCM10', 6);
