import os
import glob
import pandas as pd

ROOT = os.path.dirname(__file__)
csv_paths = sorted(glob.glob(os.path.join(ROOT, "*.csv")))

def profile_df(df: pd.DataFrame) -> dict:
    out = {}
    out["rows"] = len(df)
    out["cols"] = df.shape[1]
    out["duplicate_rows"] = int(df.duplicated().sum())
    out["missing_cells"] = int(df.isna().sum().sum())
    out["missing_by_col"] = df.isna().sum().to_dict()
    out["dtypes"] = df.dtypes.astype(str).to_dict()
    out["nunique_by_col"] = df.nunique(dropna=True).to_dict()
    return out

reports = []
for path in csv_paths:
    try:
        df = pd.read_csv(path)
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding="latin-1")
    rep = profile_df(df)
    rep["file"] = os.path.basename(path)
    rep["columns"] = list(df.columns)
    rep["head_3"] = df.head(3).to_dict(orient="records")
    reports.append(rep)

# Save a compact table
summary = pd.DataFrame([{
    "file": r["file"],
    "rows": r["rows"],
    "cols": r["cols"],
    "duplicate_rows": r["duplicate_rows"],
    "missing_cells": r["missing_cells"],
} for r in reports]).sort_values(["file"])

out_dir = os.path.join(ROOT, "reports")
os.makedirs(out_dir, exist_ok=True)

summary_path = os.path.join(out_dir, "csv_summary.csv")
summary.to_csv(summary_path, index=False)

# Save full JSON-ish report as CSV (stringified dicts) for easy viewing
details_path = os.path.join(out_dir, "csv_details.csv")
pd.DataFrame(reports).to_csv(details_path, index=False)

print("Found CSVs:", len(csv_paths))
print("Wrote:")
print(" -", summary_path)
print(" -", details_path)
print()
print(summary.to_string(index=False))
