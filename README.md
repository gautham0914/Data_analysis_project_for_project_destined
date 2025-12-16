# Data_analysis_project_for_project_destined
# Real Estate Home Value Trends (SQL + Data Architecture Case Study)

## Overview
This project analyzes state-level U.S. home value trends using a public Zillow time-series dataset (quarterly typical home value). I built a small end-to-end analytics pipeline to demonstrate:
- Data modeling + architecture (dimensional schema)
- ETL with data quality checks
- SQL analytics (growth, volatility, momentum)
- Automated refresh of results
- A minimal stakeholder-facing summary page

## Dataset
**home_v_state.csv** contains one row per state (region) and quarterly columns (e.g., Q1_2020, Q2_2020...).  
Each quarterly value represents the “typical home value” for that state in that quarter.

## Data Model (Architecture)
The raw dataset is “wide” (many quarter columns). I normalize it into a dimensional model:

### Tables
- **dim_region(region_id, state_name, size_rank)**
  - One row per state/region
  - Primary key: region_id

- **dim_time(time_id, quarter, year, quarter_num)**
  - One row per quarter
  - Primary key: time_id (constructed from year + quarter)

- **fact_home_values(region_id, time_id, median_home_value)**
  - Grain: 1 row per state per quarter
  - Composite primary key: (region_id, time_id)

### Why this structure
- Avoids repeating time/state fields in every row
- Clear grain for analytics (state x quarter)
- Easy to extend later (add more fact measures or new dimensions)

## ETL (Python → DuckDB)
ETL script: `etl/load_duckdb.py`
- Validates required columns exist
- Converts wide → long
- Cleans currency values into numeric
- Loads tables into DuckDB

Run:
```bash
python etl/load_duckdb.py
