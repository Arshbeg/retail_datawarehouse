CREATE TABLE dim_customers AS
SELECT 
    customer_id,
    first_name,
    last_name,
    loyalty_card_number,
    postal_code
FROM raw_customers

UNION ALL

-- Creating the "Anonymous" bucket for cash payers
SELECT 
    -1 AS customer_id,
    'Anonymous' AS first_name,
    'Shopper' AS last_name,
    'NONE' AS loyalty_card_number,
    'UNKNOWN' AS postal_code;