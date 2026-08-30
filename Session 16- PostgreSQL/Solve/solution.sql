---------------------------------
-- Part A: Modifying the Table --
---------------------------------

-- 1. Add a new column called email (TEXT).
ALTER TABLE members ADD COLUMN email TEXT;

-- 2. Add a CHECK constraint ensuring age is at least 0 if provided.
ALTER TABLE members ADD CONSTRAINT check_age CHECK (age >= 0);

-- 3. Rename the address column to city.
ALTER TABLE members RENAME COLUMN address TO city;

-- 4. Drop the email column again.
ALTER TABLE members DROP COLUMN email;

--------------------------------------------
-- Part B: Sorting, Aliases, and DISTINCT --
--------------------------------------------

-- 5. List all members ordered by age from oldest to youngest.
SELECT * FROM members ORDER BY age DESC;

-- 6. List all members ordered by city, then by std_name.
SELECT * FROM members ORDER BY city ASC, std_name ASC;

-- 7. List all members with NULL ages appearing last.
SELECT * FROM members ORDER BY age DESC NULLS LAST;

-- 8. Display std_name using the alias "member name".
SELECT std_name AS "member name" FROM members;

-- 9. Concatenate std_name and city into a single readable column.
SELECT std_name || ' lives in ' || city AS member_info FROM members;

-- 10. Display the distinct list of cities.
SELECT DISTINCT city FROM members;

-- 11. Use a table alias to display std_id and std_name for members with std_id > 5.
SELECT m.std_id, m.std_name FROM members m WHERE m.std_id > 5;

------------------------------------------------
-- Part C: Aggregate Functions and Pagination --
------------------------------------------------

-- 12. Count how many members live in each city.
SELECT city, COUNT(*) FROM members GROUP BY city;

-- 13. Find the average age per city.
SELECT city, AVG(age) FROM members GROUP BY city;

-- 14. Display only cities with more than one member using HAVING.
SELECT city, COUNT(*) FROM members GROUP BY city HAVING COUNT(*) > 1;

-- 15. Find the minimum and maximum salary among all members.
-- Note: Assuming there is a salary column from a previous lab
SELECT MIN(salary), MAX(salary) FROM members;

-- 16. Display the first 5 members ordered by std_id.
SELECT * FROM members ORDER BY std_id LIMIT 5;

-- 17. Display the next 5 members using OFFSET.
SELECT * FROM members ORDER BY std_id LIMIT 5 OFFSET 5;

-- 18. Calculate the OFFSET required to display page 4 with a page size of 5.
-- Offset = (page_number - 1) * page_size = (4 - 1) * 5 = 15
SELECT * FROM members ORDER BY std_id LIMIT 5 OFFSET 15;

----------------------------
-- Part D: SQL Essentials --
----------------------------

-- 19. Write a SELECT statement without a semicolon and observe what psql does.
-- SELECT * FROM members

-- 20. Write the same column alias twice: once using AS and once without AS.
SELECT std_name AS name1, std_name name2 FROM members;

-- 21. Concatenate two text values using || and verify that using + produces an error.
SELECT 'Hello' || ' World';
-- SELECT 'Hello' + ' World'; -- This would produce an error in PostgreSQL

---------------------------------
-- Part E: Creating New Tables --
---------------------------------
-- 22. Create a suppliers table
CREATE TABLE suppliers (
    supplier_id SERIAL PRIMARY KEY,
    name TEXT
);

-- 23. Insert three suppliers without specifying the IDs
INSERT INTO suppliers (name) VALUES ('Supplier A'), ('Supplier B'), ('Supplier C');

-- 24. Create the products and orders tables.
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name TEXT,
    supplier_id INT REFERENCES suppliers(supplier_id)
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(product_id),
    quantity INT,
    order_date DATE
);

-- 25. Insert: At least 4 products, At least 3 orders, Leave at least one product with no orders.
INSERT INTO products (name, supplier_id) VALUES 
('Product 1', 1), 
('Product 2', 1), 
('Product 3', 2), 
('Product 4', 3);

INSERT INTO orders (product_id, quantity, order_date) VALUES 
(1, 10, '2023-01-01'), 
(1, 5, '2023-01-02'), 
(2, 20, '2023-01-03');
-- Product 3 and 4 have no orders

-------------------
-- Part F: Joins --
-------------------

-- 26. Write an INNER JOIN to list each order with its product name.
SELECT o.order_id, p.name AS product_name, o.quantity 
FROM orders o 
INNER JOIN products p ON o.product_id = p.product_id;

-- 27. Write a LEFT JOIN to list every product, including products that have never been ordered.
SELECT p.name AS product_name, o.order_id 
FROM products p 
LEFT JOIN orders o ON p.product_id = o.product_id;

-- 28. Write a FULL JOIN and describe in a comment what additional rows it may return compared to a LEFT JOIN.
SELECT p.name AS product_name, o.order_id 
FROM products p 
FULL JOIN orders o ON p.product_id = o.product_id;

-- 29. Write a CROSS JOIN between products and orders
SELECT * FROM products CROSS JOIN orders;

-- Part G: DELETE, TRUNCATE, and DROP
-- 30. Delete a single row from orders using WHERE and verify the DELETE 1 message.
DELETE FROM orders WHERE order_id = 1;

-- 31. Truncate the orders table and verify that it is empty but still exists.
TRUNCATE TABLE orders;

-- 32. Drop the orders table and confirm that it no longer appears in \dt.
DROP TABLE orders;

-- Recreate and populate orders for the challenge since we dropped it
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(product_id),
    quantity INT,
    order_date DATE
);
INSERT INTO orders (product_id, quantity, order_date) VALUES 
(1, 10, '2023-01-01'), 
(1, 5, '2023-01-02'), 
(2, 20, '2023-01-03'),
(2, 15, '2023-01-04');

SELECT 
    p.name AS product_name, 
    COUNT(o.order_id) AS times_ordered,
    AVG(o.quantity) AS average_order_quantity
FROM 
    products p
LEFT JOIN 
    orders o ON p.product_id = o.product_id
GROUP BY 
    p.product_id, p.name
HAVING 
    COUNT(o.order_id) >= 2
ORDER BY 
    times_ordered DESC;
