CREATE TABLE dim_stores AS
SELECT 
    store_id,
    store_name,
    format AS store_format,
    region
FROM raw_stores;