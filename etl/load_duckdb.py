import re
import pandas as pd
import duckdb
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = PROJECT_ROOT / "data" / "home_v_state.csv"
DB_PATH = PROJECT_ROOT / "realestate.duckdb"

REGION_COLS = ["region_id", "state", "size_rank"]
QUARTER_REGEX = r"^Q[1-4]_\d{4}$"

def clean_money(x):
    """Convert currency-like values to float. Returns None if not parseable."""
    if pd.isna(x):
        return None
    s = str(x).strip().replace("$", "").replace(",", "")
    try:
        return float(s)
    except ValueError:
        return None

def assert_required_columns(df: pd.DataFrame) -> None:
    missing = [c for c in REGION_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

def get_quarter_columns(df: pd.DataFrame) -> list[str]:
    quarter_cols = [c for c in df.columns if re.match(QUARTER_REGEX, c)]
    if not quarter_cols:
        raise ValueError("No quarter columns found (expected Q1_YYYY format).")
    return quarter_cols

def run_quality_checks(dim_region: pd.DataFrame, dim_time: pd.DataFrame, fact: pd.DataFrame) -> None:
    # Null checks
    if dim_region["region_id"].isna().any():
        raise ValueError("dim_region has NULL region_id")
    if dim_time["time_id"].isna().any():
        raise ValueError("dim_time has NULL time_id")
    if fact[["region_id", "time_id"]].isna().any().any():
        raise ValueError("fact_home_values has NULL keys (region_id or time_id)")

    # Duplicate checks (keys)
    if dim_region["region_id"].duplicated().any():
        raise ValueError("Duplicate region_id found in dim_region")
    if dim_time["time_id"].duplicated().any():
        raise ValueError("Duplicate time_id found in dim_time")
    if fact.duplicated(subset=["region_id", "time_id"]).any():
        raise ValueError("Duplicate (region_id, time_id) rows found in fact_home_values")

def build_tables_from_csv(csv_path: Path):
    df = pd.read_csv(csv_path)
    assert_required_columns(df)
    quarter_cols = get_quarter_columns(df)

    # Keep only needed cols
    df = df[REGION_COLS + quarter_cols].copy()

    # Wide -> long
    long_df = df.melt(
        id_vars=REGION_COLS,
        value_vars=quarter_cols,
        var_name="quarter",
        value_name="median_home_value"
    )

    # Clean values
    long_df["median_home_value"] = long_df["median_home_value"].apply(clean_money)

    # Build dim_region (1 row per region_id)
    dim_region = (
        long_df[["region_id", "state", "size_rank"]]
        .drop_duplicates()
        .rename(columns={"state": "state_name"})
        .copy()
    )

    # Build dim_time (quarter -> year, quarter_num, time_id)
    time_df = long_df[["quarter"]].drop_duplicates().copy()
    time_df["quarter_num"] = time_df["quarter"].str.extract(r"Q([1-4])_").astype(int)
    time_df["year"] = time_df["quarter"].str.extract(r"_(\d{4})").astype(int)
    time_df["time_id"] = time_df["year"] * 10 + time_df["quarter_num"]
    dim_time = time_df[["time_id", "quarter", "year", "quarter_num"]].copy()

    # Build fact table (1 row per region_id per time_id)
    fact = long_df.merge(dim_time[["quarter", "time_id"]], on="quarter", how="left")
    fact_home_values = fact[["region_id", "time_id", "median_home_value"]].copy()

    # Quality checks before loading
    run_quality_checks(dim_region, dim_time, fact_home_values)

    return df, long_df, dim_region, dim_time, fact_home_values

def load_to_duckdb(db_path: Path, dim_region: pd.DataFrame, dim_time: pd.DataFrame, fact: pd.DataFrame) -> None:
    con = duckdb.connect(str(db_path))

    con.execute("DROP TABLE IF EXISTS fact_home_values;")
    con.execute("DROP TABLE IF EXISTS dim_time;")
    con.execute("DROP TABLE IF EXISTS dim_region;")

    con.execute("""
        CREATE TABLE dim_region (
            region_id BIGINT PRIMARY KEY,
            state_name TEXT NOT NULL,
            size_rank BIGINT
        );
    """)

    con.execute("""
        CREATE TABLE dim_time (
            time_id BIGINT PRIMARY KEY,
            quarter TEXT NOT NULL,
            year INTEGER NOT NULL,
            quarter_num INTEGER NOT NULL
        );
    """)

    con.execute("""
        CREATE TABLE fact_home_values (
            region_id BIGINT NOT NULL,
            time_id BIGINT NOT NULL,
            median_home_value DOUBLE,
            PRIMARY KEY (region_id, time_id)
        );
    """)

    con.register("dim_region_df", dim_region)
    con.register("dim_time_df", dim_time)
    con.register("fact_df", fact)

    con.execute("INSERT INTO dim_region SELECT * FROM dim_region_df;")
    con.execute("INSERT INTO dim_time SELECT * FROM dim_time_df;")
    con.execute("INSERT INTO fact_home_values SELECT * FROM fact_df;")

    con.close()

def main():
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"CSV not found at: {CSV_PATH}")

    df_raw, df_long, dim_region, dim_time, fact = build_tables_from_csv(CSV_PATH)
    load_to_duckdb(DB_PATH, dim_region, dim_time, fact)

    # Sanity summary
    con = duckdb.connect(str(DB_PATH))
    r = con.execute("SELECT COUNT(*) FROM dim_region;").fetchone()[0]
    t = con.execute("SELECT COUNT(*) FROM dim_time;").fetchone()[0]
    f = con.execute("SELECT COUNT(*) FROM fact_home_values;").fetchone()[0]
    nulls = con.execute("SELECT COUNT(*) FROM fact_home_values WHERE median_home_value IS NULL;").fetchone()[0]
    con.close()

    print("ETL complete.")
    print(f"dim_region rows: {r}")
    print(f"dim_time rows: {t}")
    print(f"fact_home_values rows: {f}")
    print(f"fact_home_values NULL median_home_value: {nulls}")

if __name__ == "__main__":
    main()
