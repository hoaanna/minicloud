CREATE DATABASE IF NOT EXISTS mycloud;
USE mycloud;

CREATE TABLE IF NOT EXISTS students (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_id VARCHAR(20) NULL,
  fullname VARCHAR(200) NOT NULL,
  major VARCHAR(100) NULL,
  gpa FLOAT NULL
);

INSERT INTO students (student_id, fullname, major, gpa) VALUES
('SV01', 'Nguyễn Văn A', 'IT', 3.2),
('SV02', 'Trần Thị B', 'AI', 3.4),
('SV03', 'Phạm Văn C', 'SE', 3.1);
