-- Customer table DDL
-- This table stores customer information
CREATE TABLE MST_CUSTOMER (
    id INT PRIMARY KEY,  -- Primary key
    internal_no INT REFERENCES MST_EXAMPLE(id),  -- FK using inline REFERENCES
    customer_name VARCHAR(50),  -- Customer full name
    age INT,
    gender CHAR(1),  -- m, f, or empty
    address_code VARCHAR(4),
    email VARCHAR(50),
    phone_number VARCHAR(50),
    created_at DATETIME  -- Record creation timestamp
);

/*
 * Multi-line comment example
 * This should be ignored by the parser
 */
