-- 1) Top states by average home value
SELECT
  r.state_name,
  ROUND(AVG(f.median_home_value), 2) AS avg_home_value
FROM fact_home_values f
JOIN dim_region r ON r.region_id = f.region_id
GROUP BY r.state_name
ORDER BY avg_home_value DESC
LIMIT 10;

-- 2) Growth (first quarter -> last quarter)
WITH bounds AS (
  SELECT region_id, MIN(time_id) AS first_time, MAX(time_id) AS last_time
  FROM fact_home_values
  GROUP BY region_id
),
vals AS (
  SELECT
    r.state_name,
    f1.median_home_value AS first_value,
    f2.median_home_value AS last_value
  FROM bounds b
  JOIN dim_region r ON r.region_id = b.region_id
  JOIN fact_home_values f1 ON f1.region_id=b.region_id AND f1.time_id=b.first_time
  JOIN fact_home_values f2 ON f2.region_id=b.region_id AND f2.time_id=b.last_time
)
SELECT
  state_name,
  ROUND(first_value, 2) AS first_value,
  ROUND(last_value, 2) AS last_value,
  ROUND((last_value - first_value) / NULLIF(first_value,0) * 100, 2) AS growth_pct
FROM vals
ORDER BY growth_pct DESC
LIMIT 10;

-- 3) Volatility (std dev)
SELECT
  r.state_name,
  ROUND(stddev_samp(f.median_home_value), 2) AS volatility
FROM fact_home_values f
JOIN dim_region r ON r.region_id = f.region_id
GROUP BY r.state_name
ORDER BY volatility DESC
LIMIT 10;

-- 4) QoQ growth metrics (derived columns = more insights)
SELECT
  r.state_name,
  t.year,
  t.quarter_num,
  f.median_home_value,
  ROUND(
    (f.median_home_value - LAG(f.median_home_value) OVER (PARTITION BY r.state_name ORDER BY t.year, t.quarter_num))
    / NULLIF(LAG(f.median_home_value) OVER (PARTITION BY r.state_name ORDER BY t.year, t.quarter_num), 0) * 100
  , 2) AS qoq_growth_pct
FROM fact_home_values f
JOIN dim_region r ON r.region_id = f.region_id
JOIN dim_time t ON t.time_id = f.time_id
ORDER BY r.state_name, t.year, t.quarter_num;
-- 5) YoY growth metrics (derived columns = more insights)
SELECT
  r.state_name,
  t.year,
  t.quarter_num,
  f.median_home_value,
  ROUND(
    (f.median_home_value - LAG(f.median_home_value, 4) OVER (PARTITION BY r.state_name ORDER BY t.year, t.quarter_num))
    / NULLIF(LAG(f.median_home_value, 4) OVER (PARTITION BY r.state_name ORDER BY t.year, t.quarter_num), 0) * 100
  , 2) AS yoy_growth_pct
FROM fact_home_values f
JOIN dim_region r ON r.region_id = f.region_id
JOIN dim_time t ON t.time_id = f.time_id
ORDER BY r.state_name, t.year, t.quarter_num;

-- 6) Most expensive AND fastest growing
WITH avg_vals AS (
  SELECT r.state_name, AVG(f.median_home_value) AS avg_value
  FROM fact_home_values f
  JOIN dim_region r ON r.region_id=f.region_id
  GROUP BY r.state_name
),
growth AS (
  WITH bounds AS (
    SELECT region_id, MIN(time_id) AS first_time, MAX(time_id) AS last_time
    FROM fact_home_values GROUP BY region_id
  ),
  vals AS (
    SELECT r.state_name,
           f1.median_home_value AS first_value,
           f2.median_home_value AS last_value
    FROM bounds b
    JOIN dim_region r ON r.region_id=b.region_id
    JOIN fact_home_values f1 ON f1.region_id=b.region_id AND f1.time_id=b.first_time
    JOIN fact_home_values f2 ON f2.region_id=b.region_id AND f2.time_id=b.last_time
  )
  SELECT state_name,
         (last_value-first_value)/NULLIF(first_value,0) * 100 AS growth_pct
  FROM vals
)
SELECT
  a.state_name,
  ROUND(a.avg_value,2) AS avg_value,
  ROUND(g.growth_pct,2) AS growth_pct
FROM avg_vals a
JOIN growth g USING (state_name)
ORDER BY avg_value DESC, growth_pct DESC
LIMIT 10;

-- 7) Recent momentum” (last 2 quarters growth)
WITH ordered AS (
  SELECT
    r.state_name,
    t.year,
    t.quarter_num,
    f.median_home_value,
    ROW_NUMBER() OVER (PARTITION BY r.state_name ORDER BY t.year DESC, t.quarter_num DESC) AS rn
  FROM fact_home_values f
  JOIN dim_region r ON r.region_id=f.region_id
  JOIN dim_time t ON t.time_id=f.time_id
),
last2 AS (
  SELECT
    state_name,
    MAX(CASE WHEN rn=1 THEN median_home_value END) AS latest,
    MAX(CASE WHEN rn=3 THEN median_home_value END) AS two_quarters_ago
  FROM ordered
  GROUP BY state_name
)
SELECT
  state_name,
  ROUND((latest-two_quarters_ago)/NULLIF(two_quarters_ago,0)*100,2) AS last_2q_growth_pct
FROM last2
ORDER BY last_2q_growth_pct DESC
LIMIT 10;
