from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_ROOT / "results"
OUT_MD = RESULTS_DIR / "report.md"

SECTIONS = [
    ("Top states by average home value", "01_top_avg_home_value.csv"),
    ("Top states by growth (first quarter to last quarter)", "02_growth_first_last.csv"),
    ("Most volatile states (std dev of home values)", "03_volatility.csv"),
    ("Quarter-over-quarter growth by state and quarter", "04_qoq_growth.csv"),
    ("Year-over-year growth by state and quarter", "05_yoy_growth.csv"),
    ("High value + high growth (combined ranking)", "06_high_value_high_growth.csv"),
    ("Recent momentum (last 2 quarters growth)", "07_recent_momentum.csv"),
]

def df_to_md(df: pd.DataFrame, max_rows: int = 15) -> str:
    note = ""
    if len(df) > max_rows:
        df = df.head(max_rows)
        note = f"\n\n_Showing first {max_rows} rows. Full output is in the CSV file._\n"
    return df.to_markdown(index=False) + note

def main():
    RESULTS_DIR.mkdir(exist_ok=True)

    lines = []
    lines.append("# Real Estate SQL Results\n")
    lines.append("This report lists each analytical question and its output table.\n")

    for title, fname in SECTIONS:
        path = RESULTS_DIR / fname
        lines.append(f"## {title}\n")
        lines.append(f"Source CSV: `{fname}`\n")

        if not path.exists():
            lines.append("\nMissing CSV file.\n\n---\n")
            continue

        df = pd.read_csv(path)
        lines.append("\n" + df_to_md(df) + "\n")
        lines.append("\n---\n")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote: {OUT_MD}")

if __name__ == "__main__":
    main()
