-- ########################################
-- Lab Solution (Pages 11 and 12)
-- ########################################

-- ########################################
--     Lab Part A: CHECK and UNIQUE
-- ########################################
CREATE TABLE products (
    product_id integer PRIMARY KEY,
    name text UNIQUE,
    price numeric CHECK (price > 0)
);

INSERT INTO products (product_id, name, price) VALUES (1, 'Laptop', 1000);


-- ########################################
--        Lab Part B: DEFAULT
-- ########################################

CREATE TABLE orders (
    order_id integer PRIMARY KEY,
    product_id integer REFERENCES products(product_id),
    quantity numeric DEFAULT 1
);

INSERT INTO orders (order_id, product_id) VALUES (1, 1);
SELECT * FROM orders WHERE order_id = 1;


-- ########################################
-- Lab Part C: Foreign Key Enforcement
-- ########################################

INSERT INTO products (product_id, name, price) VALUES (2, 'Mouse', 50);

INSERT INTO orders (order_id, product_id, quantity) VALUES (2, 2, 5);

-- INSERT INTO orders (order_id, product_id, quantity) VALUES (3, 3, 1); => Error

-- ########################################
-- Lab Part D: Referential Integrity on Delete
-- ########################################

-- DELETE FROM products WHERE product_id = 1; => Error
DELETE FROM orders WHERE product_id = 1;
DELETE FROM products WHERE product_id = 1;


-- ########################################
-- Lab Part E: RESTRICT versus CASCADE
-- ########################################

DROP TABLE orders;
CREATE TABLE orders (
    order_id integer PRIMARY KEY,
    product_id integer REFERENCES products(product_id) ON DELETE CASCADE,
    quantity numeric DEFAULT 1
);

INSERT INTO products (product_id, name, price) VALUES (3, 'Keyboard', 150);
INSERT INTO orders (order_id, product_id, quantity) VALUES (3, 3, 2);

DELETE FROM products WHERE product_id = 3;
SELECT * FROM orders WHERE product_id = 3;


-- ########################################
-- Practical Challenge
-- ########################################

-- 1. Create categories table
CREATE TABLE categories (
    category_id integer PRIMARY KEY,
    category_name text UNIQUE NOT NULL
);

ALTER TABLE products 
ADD COLUMN category_id integer REFERENCES categories(category_id) ON DELETE RESTRICT;

INSERT INTO categories (category_id, category_name) VALUES (1, 'Electronics');
INSERT INTO categories (category_id, category_name) VALUES (2, 'Accessories');
INSERT INTO categories (category_id, category_name) VALUES (3, 'Office Supplies');

UPDATE products SET category_id = 2 WHERE product_id = 2;

INSERT INTO products (product_id, name, price, category_id) VALUES (4, 'Monitor', 2000, 1);

