CREATE DATABASE IF NOT EXISTS hr_analytics;
USE hr_analytics;

-- Table for Clean Employee Records
CREATE TABLE IF NOT EXISTS clean_employees (
    emp_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    full_name VARCHAR(100),
    email VARCHAR(100),
    department VARCHAR(50),
    joining_date DATE,
    base_salary DECIMAL(10, 2)
);

-- Table for Logging Validation Exceptions
CREATE TABLE IF NOT EXISTS data_exceptions (
    exception_id INT AUTO_INCREMENT PRIMARY KEY,
    emp_id VARCHAR(20),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    department VARCHAR(50),
    issue_reason VARCHAR(255),
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
