CREATE TABLE fact_inventory_daily_snapshot AS
SELECT 
    -- 1. The Snapshot Date (Using today's date)
    CURRENT_DATE AS snapshot_date,
    
    -- 2. The Dimensions
    ds.store_id,
    dp.product_id,
    
    -- 3. The Measures (Simulating inventory levels)
    -- Generating a random stock level between 0 and 250
    FLOOR(RANDOM() * 250)::INT AS quantity_on_hand,
    
    -- Simulating damaged/spoiled goods (10% chance a product has 1-5 damaged items)
    CASE 
        WHEN RANDOM() > 0.90 THEN FLOOR(RANDOM() * 5 + 1)::INT 
        ELSE 0 
    END AS quantity_damaged

FROM dim_stores ds
CROSS JOIN dim_products dp;