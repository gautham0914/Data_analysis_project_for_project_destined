# Data_analysis_project_for_project_destined
# Real Estate Data Analytics & Workflow Automation Case Study

## Overview
This project analyzes **state-level U.S. home value trends** using a public Zillow quarterly time-series dataset.

The goal is to demonstrate how raw housing data can be transformed into **clean, decision-ready insights** using:
- Proper data modeling
- ETL pipelines
- Analytical SQL
- Automated refresh workflows
- Clear stakeholder communication

This project is intentionally designed as a **real-world analytics case study**, not a one-off script.

---

## Dataset

**Source:** Zillow Home Value Index (ZHVI) – State level  
**Granularity:** Quarterly  
**Metric:** Typical home value (USD)

The raw dataset (`home_v_state.csv`) is structured in a **wide format**, with one row per state and many quarterly columns (e.g., `Q1_2020`, `Q2_2020`, …).

---

## Data Architecture (Dimensional Model)

To support scalable analytics, the dataset is normalized into a **star schema**.

### Tables

#### `dim_region`
- `region_id` (PK)
- `state_name`
- `size_rank`

One row per U.S. state.

#### `dim_time`
- `time_id` (PK)
- `year`
- `quarter`
- `quarter_num`

One row per quarter.

#### `fact_home_values`
- `region_id` (FK)
- `time_id` (FK)
- `median_home_value`

**Grain:** One row per *state × quarter*.

### Why this model?

- Prevents duplicated time/state fields
- Makes trends easy to calculate
- Matches real production analytics schemas
- Easily extensible (new metrics, regions, or datasets)

---

## ETL Pipeline (Python → DuckDB)

**Script:** `etl/load_duckdb.py`

The ETL process:
1. Validates required columns
2. Converts wide → long format
3. Cleans numeric values
4. Loads dimension and fact tables
5. Writes everything to DuckDB

DuckDB is used because it supports:
- Analytical SQL
- Local reproducibility
- Fast execution in CI/CD pipelines

---

## SQL Analytics Layer

**SQL file:** `sql/analysis.sql`

The SQL layer is responsible for **business logic**, not data ingestion.

### Questions answered

- Which states have the highest average home values?
- How have prices changed from the first to latest quarter?
- Which markets are most volatile?
- How strong is quarter-over-quarter growth?
- How do year-over-year trends differ?
- Which states show recent momentum?
- How do value and growth compare together?

### Outputs

All queries write results to the `results/` directory:

- **CSV files** → machine-readable outputs
- **`report.md`** → human-readable stakeholder summary

---

## Automation (GitHub Actions)

**Workflow:** `.github/workflows/pipeline.yml`

On every push to `main`, the pipeline:
1. Installs dependencies
2. Runs the ETL pipeline
3. Executes SQL analytics
4. Regenerates result files
5. Commits refreshed outputs automatically

This simulates a **production analytics refresh cycle**.

---

## Key Insights (Executive Summary)

This analysis shows that **price, growth, volatility, and momentum must be evaluated together**.

### High-level findings

- **High prices are structural**, not necessarily fast-growing  
  (e.g., coastal states remain expensive due to long-term supply constraints)

- **Fast growth often appears in mid-priced markets**, not the most expensive ones

- **Average prices hide risk**  
  Some states show high volatility despite stable averages

- **Short-term momentum can diverge from long-term trends**  
  Recent slowdowns may follow years of strong growth

- **Different metrics answer different questions**  
  QoQ highlights momentum, YoY reflects sustained change

📄 **Detailed explanations:**  
👉 [`insights/insights.md`](insights/insights.md)

---

## Quick Links

- 📊 **Stakeholder report:** [`results/report.md`](results/report.md)
- 📁 **All results (CSV):** [`results/`](results/)
- 🧠 **SQL logic:** [`sql/analysis.sql`](sql/analysis.sql)
- ⚙️ **ETL pipeline:** [`etl/load_duckdb.py`](etl/load_duckdb.py)
- 🔁 **Automation workflow:** [`.github/workflows/pipeline.yml`](.github/workflows/pipeline.yml)






## Frontend (Next.js + Tailwind)

- 🚀 Live site: https://realestate-casestudy.vercel.app
- 📂 Source (App Router): `app/`
  - Page: `app/page.tsx` (hero + image card + overview, insights, tables)
  - Layout + styles: `app/layout.tsx`, `app/globals.css`
  - CSV loader: `lib/csv.ts` (reads `results/*.csv` at build time)
  - Background images: `public/images/city-skyline.jpg`, `public/images/buildings.jpg`

What the page shows
- Hero with Project Destined context + quick links
- Prominent city skyline image card above Project Overview
- Clear “Key Insights” with plain-language subtitles
- Data Highlights tables (Top Avg Value, Top Growth, Volatility, Momentum)

Local development
```bash
npm install
npm run dev
# build for deploy
npm run build
```

Vercel
- Build command: `npm run build`
- Output: `.next` (default)
- No server/API required; static-friendly build reading CSVs from `results/`







