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

## SQL Analysis

SQL analysis is implemented in `sql/analysis.sql` and runs on the normalized DuckDB tables created during the ETL step.

This layer represents the **analytical business logic** of the project, separating raw data ingestion from insights generation.

### Analytical focus

The SQL analysis answers the following questions:

- What are the average home values by state?
- How have home values changed over the long term (first quarter → latest quarter)?
- Which states exhibit higher or lower price volatility?
- How do markets behave quarter-over-quarter (QoQ)?
- How do year-over-year (YoY) trends differ from short-term movement?
- Which markets show recent momentum or deceleration?
- How do value levels and growth rates compare when viewed together?

### Output artifacts

All SQL outputs are exported as structured CSV files into the `results/` directory.

- **Machine-readable outputs:** `results/*.csv`
- **Human-readable summary:** `results/report.md`

The written report presents:
- Each analytical question in plain language
- The resulting tables generated from SQL
- Clean formatting suitable for non-technical stakeholders

### Data quality & validation

Before generating analytical outputs, the SQL layer enforces validation checks to ensure:

- One record per state per quarter (no duplicate grain)
- Acceptable null rates in key fact measures
- Consistent time coverage across regions

If validation fails, downstream result tables are not refreshed.

### Why this SQL layer matters

This approach mirrors production analytics workflows by:

- Separating **raw data** from **analytical logic**
- Making results easier to audit and explain
- Enabling safe, automated refreshes
- Supporting reuse in dashboards, lessons, or case studies

The SQL layer is intentionally designed to be extensible as new metrics, regions, or educational use cases are added.

---
## Key Insights

This analysis examines how U.S. home values behave over time by looking at **price levels, growth, volatility, and recent momentum together** rather than in isolation.

The key findings are:

- **High home prices are usually structural.**  
  States with the highest average home values (e.g., Hawaii, California) are expensive because of long-term supply and demand conditions, not because of recent rapid growth.

- **Fast growth often happens in mid-priced markets.**  
  Many of the fastest-growing states started from moderate price levels, showing that strong appreciation does not require already-expensive housing markets.

- **Average prices hide risk.**  
  Some states with high or stable average prices still experience large quarter-to-quarter swings, meaning volatility is an important risk signal that averages alone do not show.

- **Recent trends can differ from long-term performance.**  
  States with strong multi-year growth can show slowing momentum in recent quarters, while other states may show short-term acceleration despite weaker long-term trends.

- **Different metrics answer different questions.**  
  Quarter-over-quarter growth highlights short-term movement, while year-over-year growth better reflects sustained trends. Using both provides a more responsible view of market behavior.

Together, these insights show that **price, growth, stability, and momentum must be evaluated jointly** to understand housing markets properly.

📄 **Detailed explanations and examples:** [`insights/insights.md`](insights/insights.md)
