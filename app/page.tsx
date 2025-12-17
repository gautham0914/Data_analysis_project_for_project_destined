import fs from "fs";
import path from "path";
import { parseCsv } from "../lib/csv";

export const dynamic = "force-static";

type TableRow = { state: string; value: number };

type Dataset = {
  topValues: TableRow[];
  topGrowth: TableRow[];
  volatility: TableRow[];
  momentum: TableRow[];
};

const DATA_FILES = {
  topValues: "results/01_top_avg_home_value.csv",
  topGrowth: "results/02_growth_first_last.csv",
  volatility: "results/03_volatility.csv",
  momentum: "results/07_recent_momentum.csv"
};

function safeReadCsv(relativePath: string) {
  try {
    const fullPath = path.join(process.cwd(), relativePath);
    const content = fs.readFileSync(fullPath, "utf-8");
    return parseCsv(content);
  } catch (err) {
    console.warn(`Missing or unreadable file: ${relativePath}`, err);
    return [];
  }
}

function buildTable(rows: ReturnType<typeof parseCsv>, valueKey: string): TableRow[] {
  return rows
    .slice(0, 10)
    .map((row) => ({ state: row["state_name"] ?? "", value: Number(row[valueKey] ?? 0) }))
    .filter((row) => row.state);
}

function formatCurrency(value: number) {
  if (!Number.isFinite(value)) return "Data not available";
  return `$${value.toLocaleString("en-US", { maximumFractionDigits: 0 })}`;
}

function formatPercent(value: number) {
  if (!Number.isFinite(value)) return "Data not available";
  return `${value.toFixed(2)}%`;
}

function loadData(): Dataset {
  const topValues = buildTable(safeReadCsv(DATA_FILES.topValues), "avg_home_value");
  const topGrowth = buildTable(safeReadCsv(DATA_FILES.topGrowth), "growth_pct");
  const volatility = buildTable(safeReadCsv(DATA_FILES.volatility), "volatility");
  const momentum = buildTable(safeReadCsv(DATA_FILES.momentum), "last_2q_growth_pct");

  return { topValues, topGrowth, volatility, momentum };
}

const overviewItems = [
  "Data gathered and cleaned with Python",
  "Organized so state trends are easy to compare",
  "Key trends calculated with SQL (growth, risk, momentum)",
  "Results auto-refresh on each update"
];

const insights = [
  {
    title: "Highest-priced states are not always the fastest growing.",
    subtitle: "Growth = % change from the first available quarter to the latest quarter."
  },
  {
    title: "Fast growth often comes from mid-priced states, not the top three.",
    subtitle: "Compare starting price rank with total growth rank."
  },
  {
    title: 'Averages can hide risk; volatility changes which markets look "safe".',
    subtitle: "Volatility = the typical dollar ups and downs each quarter."
  },
  {
    title: "Recent momentum can disagree with the long-term trend.",
    subtitle: "Momentum = last 2 quarters' % change; trend = full-period % change."
  },
  {
    title: "Quarter-over-quarter and year-over-year answer different questions.",
    subtitle: "QoQ shows short-term movement; YoY shows seasonality-aware direction."
  }
];

function DataTable({
  title,
  caption,
  rows,
  formatter,
  columnLabel
}: {
  title: string;
  caption: string;
  rows: TableRow[];
  formatter: (value: number) => string;
  columnLabel: string;
}) {
  const hasData = rows.length > 0;
  return (
    <div className="rounded-2xl bg-card/80 border border-slate-800 shadow-glow p-6 flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-slate-50">{title}</h3>
        <span className="text-xs uppercase tracking-wide text-slate-400">Top 10</span>
      </div>
      <p className="text-sm text-slate-400">{caption}</p>
      {hasData ? (
        <table className="w-full text-sm">
          <thead>
            <tr className="text-slate-400">
              <th className="text-left pb-2">State</th>
              <th className="text-right pb-2">{columnLabel}</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {rows.map((row) => (
              <tr key={row.state} className="text-slate-100">
                <td className="py-2 pr-2">{row.state}</td>
                <td className="py-2 text-right font-medium text-slate-50">{formatter(row.value)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p className="text-slate-400">Data not available.</p>
      )}
    </div>
  );
}

export default function Page() {
  const data = loadData();

  return (
    <main className="max-w-6xl mx-auto px-4 py-16 space-y-16">
      <section className="grid lg:grid-cols-2 gap-10 items-center">
        <div className="space-y-6">
          <div className="inline-flex items-center gap-2 rounded-full border border-slate-800 bg-slate-900/60 px-3 py-1 text-xs text-slate-300">
            <span className="h-2 w-2 rounded-full bg-sky-400 animate-pulse" />
            Built for Project Destined
          </div>
          <div className="space-y-3">
            <p className="text-sm text-slate-400 uppercase tracking-[0.2em]">Gautham Gongada</p>
            <h1 className="text-3xl sm:text-4xl font-bold text-slate-50 leading-tight">
              Real Estate Data Analytics & Workflow Automation Case Study
            </h1>
            <p className="text-sky-200 font-semibold">
              Built specifically for Project Destined: Python, SQL, data modeling, and automated refresh
            </p>
            <p className="text-lg text-slate-300">
              I built this end-to-end for Project Destined to showcase Python data work, SQL analysis, automation, and clear stakeholder reporting across U.S. housing data.
            </p>
          </div>
          <div className="grid sm:grid-cols-2 gap-3">
            <a className="rounded-xl bg-sky-500 text-slate-950 font-semibold px-4 py-3 text-center hover:bg-sky-400 transition" href="https://github.com/gautham0914/data_analysis_project_for_project_destined" target="_blank" rel="noreferrer">
              GitHub Repo
            </a>
            <a className="rounded-xl border border-slate-800 bg-slate-900/60 px-4 py-3 text-center hover:border-sky-500 transition" href="https://github.com/gautham0914/data_analysis_project_for_project_destined/blob/main/results/report.md" target="_blank" rel="noreferrer">
              Stakeholder Report
            </a>
            <a className="rounded-xl border border-slate-800 bg-slate-900/60 px-4 py-3 text-center hover:border-sky-500 transition" href="https://github.com/gautham0914/data_analysis_project_for_project_destined/blob/main/insights/insights.md" target="_blank" rel="noreferrer">
              Insights File
            </a>
            <a className="rounded-xl border border-slate-800 bg-slate-900/60 px-4 py-3 text-center hover:border-sky-500 transition" href="https://github.com/gautham0914/data_analysis_project_for_project_destined/blob/main/sql/analysis.sql" target="_blank" rel="noreferrer">
              SQL Analysis
            </a>
            <a className="rounded-xl border border-slate-800 bg-slate-900/60 px-4 py-3 text-center hover:border-sky-500 transition" href="https://github.com/gautham0914/data_analysis_project_for_project_destined/blob/main/etl/load_duckdb.py" target="_blank" rel="noreferrer">
              ETL Pipeline
            </a>
            <a className="rounded-xl border border-slate-800 bg-slate-900/60 px-4 py-3 text-center hover:border-sky-500 transition" href="https://github.com/gautham0914/data_analysis_project_for_project_destined/blob/main/.github/workflows/pipeline.yml" target="_blank" rel="noreferrer">
              Automation Workflow
            </a>
            <a className="rounded-xl border border-slate-800 bg-slate-900/60 px-4 py-3 text-center hover:border-sky-500 transition" href="https://www.linkedin.com/in/gauthamgongada" target="_blank" rel="noreferrer">
              LinkedIn
            </a>
            <a className="rounded-xl border border-slate-800 bg-slate-900/60 px-4 py-3 text-center hover:border-sky-500 transition" href="https://gauthamgongada.com" target="_blank" rel="noreferrer">
              Portfolio
            </a>
          </div>
        </div>
        <div className="space-y-6">
          <div className="rounded-2xl border border-slate-800 bg-slate-900/60 overflow-hidden shadow-glow">
            <img
              src="/images/city-skyline.jpg"
              alt="City skyline contextual image"
              className="w-full h-56 sm:h-64 lg:h-72 object-cover object-center"
            />
          </div>
          <div className="rounded-2xl border border-slate-800 bg-card/80 shadow-glow p-6 space-y-6">
            <h2 className="text-xl font-semibold">Project Overview</h2>
            <ul className="space-y-3 text-slate-300">
              {overviewItems.map((item) => (
                <li key={item} className="flex gap-3 items-start">
                  <span className="mt-1 h-2 w-2 rounded-full bg-sky-400" />
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </section>

      <section className="space-y-4">
        <h2 className="text-2xl font-semibold">Key Insights</h2>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {insights.map((item) => (
            <div key={item.title} className="rounded-2xl bg-card/80 border border-slate-800 p-5 shadow-glow">
              <p className="text-slate-200 font-semibold">{item.title}</p>
              <p className="text-xs text-slate-400 mt-1">{item.subtitle}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="space-y-6">
        <div className="flex flex-col gap-2">
          <h2 className="text-2xl font-semibold">Data Highlights</h2>
          <p className="text-slate-400">Top 10 states for each metric. Dollar values show typical home prices; percentages show growth rates.</p>
        </div>
        <div className="grid lg:grid-cols-2 gap-6">
          <DataTable
            title="Top Avg Home Value"
            caption="States with the highest average typical home value across the full time range."
            rows={data.topValues}
            formatter={formatCurrency}
            columnLabel="$ Avg Home Value"
          />
          <DataTable
            title="Top Growth (first to latest quarter)"
            caption="States with the largest total % increase from the first quarter to the most recent quarter."
            rows={data.topGrowth}
            formatter={formatPercent}
            columnLabel="Total Growth %"
          />
          <DataTable
            title="Most Volatile (quarter-to-quarter swings)"
            caption="States with the biggest typical $ swings per quarter (higher = riskier variability)."
            rows={data.volatility}
            formatter={formatCurrency}
            columnLabel="Volatility ($ Std Dev)"
          />
          <DataTable
            title="Recent Momentum (last 2 quarters)"
            caption="States with the strongest short-term acceleration in the last two quarters of data."
            rows={data.momentum}
            formatter={formatPercent}
            columnLabel="Momentum % (2Q)"
          />
        </div>
      </section>
    </main>
  );
}
