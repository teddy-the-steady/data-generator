-- Example table DDL
/* This is the master table that MST_CUSTOMER references */
CREATE TABLE MST_EXAMPLE (
    id INT PRIMARY KEY,  -- Referenced by MST_CUSTOMER.internal_no
    content VARCHAR(30),
    trade_start DATE,  -- Trade start date
    trade_end DATE,    -- Trade end date
    price DECIMAL(15,2),  -- Price with 2 decimal places
    release_year INT
);
-- End of table definition
