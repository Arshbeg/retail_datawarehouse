CREATE TABLE dim_products AS
SELECT 
    product_id,
    product_name,
    category,
    sub_category,
    brand,
    unit_price,
    cost_price,
    -- Derived analytical column:
    ROUND(((unit_price - cost_price) / unit_price) * 100, 2) AS profit_margin_pct
FROM raw_products;