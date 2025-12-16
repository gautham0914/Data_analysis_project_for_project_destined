import re
import pandas as pd
import duckdb
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]  # pd-realestate-sql-case-study/
CSV_PATH = PROJECT_ROOT / "data" / "home_v_state.csv"
DB_PATH = PROJECT_ROOT / "realestate.duckdb"

def clean_money(x):
    if pd.isna(x):
        return None
    s = str(x).strip().replace("$", "").replace(",", "")
    try:
        return float(s)
    except:
        return None

def main():
    print("✅ STARTING ETL")
    print("CSV PATH:", CSV_PATH)
    print("DB  PATH:", DB_PATH)

    if not CSV_PATH.exists():
        raise FileNotFoundError(f"CSV not found at: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)
    print("✅ CSV loaded. Shape:", df.shape)

    # quarterly columns like Q1_2020
    quarter_cols = [c for c in df.columns if re.match(r"^Q[1-4]_\d{4}$", c)]
    print("✅ Found quarter columns:", len(quarter_cols))

    region_cols = ["region_id", "state", "size_rank"]
    missing = [c for c in region_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in CSV: {missing}")

    df = df[region_cols + quarter_cols].copy()

    long_df = df.melt(
        id_vars=region_cols,
        value_vars=quarter_cols,
        var_name="quarter",
        value_name="median_home_value"
    )
    print("✅ Wide → long done. Shape:", long_df.shape)

    long_df["median_home_value"] = long_df["median_home_value"].apply(clean_money)

    # dim_region
    dim_region = (
        long_df[["region_id", "state", "size_rank"]]
        .drop_duplicates()
        .rename(columns={"state": "state_name"})
        .copy()
    )

    # dim_time
    time_df = long_df[["quarter"]].drop_duplicates().copy()
    time_df["quarter_num"] = time_df["quarter"].str.extract(r"Q([1-4])_").astype(int)
    time_df["year"] = time_df["quarter"].str.extract(r"_(\d{4})").astype(int)
    time_df["time_id"] = time_df["year"] * 10 + time_df["quarter_num"]

    dim_time = time_df[["time_id", "quarter", "year", "quarter_num"]].copy()

    # fact
    fact = long_df.merge(dim_time[["quarter", "time_id"]], on="quarter", how="left")
    fact_home_values = fact[["region_id", "time_id", "median_home_value"]].copy()

    print("✅ Building DuckDB tables...")

    con = duckdb.connect(str(DB_PATH))

    con.execute("DROP TABLE IF EXISTS fact_home_values;")
    con.execute("DROP TABLE IF EXISTS dim_time;")
    con.execute("DROP TABLE IF EXISTS dim_region;")

    con.execute("""
        CREATE TABLE dim_region (
            region_id BIGINT PRIMARY KEY,
            state_name TEXT,
            size_rank BIGINT
        );
    """)

    con.execute("""
        CREATE TABLE dim_time (
            time_id BIGINT PRIMARY KEY,
            quarter TEXT,
            year INTEGER,
            quarter_num INTEGER
        );
    """)

    con.execute("""
        CREATE TABLE fact_home_values (
            region_id BIGINT,
            time_id BIGINT,
            median_home_value DOUBLE,
            PRIMARY KEY (region_id, time_id)
        );
    """)

    con.register("dim_region_df", dim_region)
    con.register("dim_time_df", dim_time)
    con.register("fact_df", fact_home_values)

    con.execute("INSERT INTO dim_region SELECT * FROM dim_region_df;")
    con.execute("INSERT INTO dim_time SELECT * FROM dim_time_df;")
    con.execute("INSERT INTO fact_home_values SELECT * FROM fact_df;")

    r = con.execute("SELECT COUNT(*) FROM dim_region;").fetchone()[0]
    t = con.execute("SELECT COUNT(*) FROM dim_time;").fetchone()[0]
    f = con.execute("SELECT COUNT(*) FROM fact_home_values;").fetchone()[0]

    print("🎉 DONE")
    print("dim_region rows:", r)
    print("dim_time rows:", t)
    print("fact_home_values rows:", f)

    con.close()

if __name__ == "__main__":
    main()
