-- ########################################
-- 01 Question 1: Create a Database and Table
-- ########################################
Create database company_db;

\c company_db;

Create Table employees(
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(20),
    age INT CHECK (age >= 18),
    salary NUMERIC CHECK (salary >= 0)
);

\d employees;
-- ########################################
-- 02 Question 2: Insert and Retrieve Data
-- ########################################
INSERT INTO employees (first_name, last_name, phone, age, salary)
VALUES
    ('Ahmed', 'Hassan', '01012345678', 30, 65000),
    ('Sara', 'Ali', '01198765432', 25, 55000),
    ('Mariam', 'Mostafa', '01234567890', 35, 72000);

SELECT * FROM employees;

INSERT INTO employees (first_name, last_name, phone, age, salary)
VALUES ('Omar', 'Khaled', '01512345678', 28, 60000)
RETURNING *;

-- ########################################
-- 03 Question 3: Database Management and Validation
-- ########################################

-- 1. List all databases in PostgreSQL.
\l

-- 2. Connect to company_db.
\c company_db;

-- 3. Attempt to insert an employee whose age is 16.
-- What happens: It fails with an error (violates check constraint "employees_age_check").
-- Explain why: Because we added a CHECK (age >= 18) constraint when creating the table.
INSERT INTO employees (first_name, last_name, phone, age, salary)
VALUES ('Test', 'Age', '01111111111', 16, 50000);

-- 4. Attempt to insert an employee with a negative salary.
-- What happens: It fails with an error (violates check constraint "employees_salary_check").
-- This is because of the CHECK (salary >= 0) constraint.
INSERT INTO employees (first_name, last_name, phone, age, salary)
VALUES ('Test', 'Salary', '01222222222', 25, -5000);

-- 5. Try to drop company_db while connected to it.
-- ERROR: cannot drop the currently open database
-- DROP DATABASE company_db; 

-- The correct steps to delete the database safely:
-- Step A: Connect to a different database (e.g., the default postgres db)
\c postgres;
-- Step B: Now you can safely drop it
-- DROP DATABASE company_db;
