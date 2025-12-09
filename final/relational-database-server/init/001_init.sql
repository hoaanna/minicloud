CREATE DATABASE IF NOT EXISTS minicloud;
USE minicloud;
CREATE TABLE IF NOT EXISTS notes(
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO notes(title) VALUES ('Hello from MariaDB!');
CREATE DATABASE IF NOT EXISTS studentdb;
USE studentdb;
CREATE TABLE IF NOT EXISTS students(
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id VARCHAR(10),
    fullname VARCHAR(100),
    dob DATE,
    major VARCHAR(50)
);
INSERT INTO students (student_id, fullname, dob, major)
VALUES
('SV001', 'Nguyen Van A', '2002-05-10', 'Information Technology'),
('SV002', 'Tran Thi B', '2001-11-22', 'Computer Science'),
('SV003', 'Le Hoang C', '2003-03-18', 'Software Engineering');

