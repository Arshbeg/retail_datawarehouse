CREATE TABLE fact_sales AS
SELECT 
    s.transaction_id,
    s.receipt_id,
    s.store_id,
    COALESCE(s.customer_id, -1) AS customer_id, -- Maps NULLs to the Anonymous row
    s.product_id,
    
    -- Time Dimensions
    CAST(s.transaction_date AS DATE) AS sale_date,
    s.transaction_date AS sale_timestamp,
    
    -- Measures
    s.quantity,
    s.gross_amount AS revenue_amount,
    
    -- Calculated Financials
    (p.cost_price * s.quantity) AS total_cost_amount,
    (s.gross_amount - (p.cost_price * s.quantity)) AS net_profit

FROM raw_sales s
LEFT JOIN raw_products p 
    ON s.product_id = p.product_id;