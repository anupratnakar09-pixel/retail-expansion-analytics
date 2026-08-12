-- ====================================================================
-- General IT Control (GITC) Data Validation Script
-- Objective: Identify and quarantine data anomalies prior to modeling
-- ====================================================================

-- Step 1: Detect Duplicate Location Entries
SELECT store_id, location_code, COUNT(*) AS duplicate_count
FROM raw_regional_sales
GROUP BY store_id, location_code
HAVING COUNT(*) > 1;

-- Step 2: Validate Data Integrity (Null Keys & Negative Revenue Anomalies)
SELECT *
FROM raw_regional_sales
WHERE store_id IS NULL
   OR location_code IS NULL
   OR total_revenue <= 0
   OR latitude NOT BETWEEN -90 AND 90
   OR longitude NOT BETWEEN -180 AND 180;

-- Step 3: Create Cleaned Data Table (GITC Compliant)
CREATE TABLE cleaned_regional_sales AS
SELECT DISTINCT
    CAST(store_id AS VARCHAR(50)) AS store_id,
    TRIM(location_code) AS location_code,
    CAST(total_revenue AS DECIMAL(12, 2)) AS total_revenue,
    CAST(latitude AS FLOAT) AS latitude,
    CAST(longitude AS FLOAT) AS longitude,
    region_zone
FROM raw_regional_sales
WHERE store_id IS NOT NULL
  AND total_revenue > 0
  AND latitude BETWEEN -90 AND 90
  AND longitude BETWEEN -180 AND 180;
