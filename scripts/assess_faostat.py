"""Workflow step: quality assessment of the raw FAOSTAT undernourishment data (before cleaning).

Run from the project folder:  python scripts/assess_faostat.py

Reads data/raw/faostat_food_security.zip, keeps the "Prevalence of undernourishment
(3-year average)" rows, and checks accuracy, completeness, timeliness and consistency.
Prints the results and saves them to reports/faostat_quality.txt. It does not change any data.
"""
import zipfile
from pathlib import Path

import pandas as pd
import pycountry

PROJECT = Path(__file__).resolve().parent.parent
RAW_FILE = PROJECT / "data" / "raw" / "faostat_food_security.zip"
REPORT_FILE = PROJECT / "reports" / "faostat_quality.txt"
DATA_CSV = "Food_Security_Data_E_All_Data_(Normalized).csv"
POU_ITEM_CODE = "210041"  

lines = []


def report(text=""):
    print(text)
    lines.append(text)


def to_iso3(m49_code):
    country = pycountry.countries.get(numeric=m49_code)
    return country.alpha_3 if country else None


with zipfile.ZipFile(RAW_FILE) as archive:
    df = pd.read_csv(archive.open(DATA_CSV), dtype=str)
pou = df[(df["Item Code"] == POU_ITEM_CODE) & (df["Element"] == "Value")].copy()

pou["m49"] = pou["Area Code (M49)"].str.lstrip("'")             # "'004" -> "004"
pou["iso3"] = pou["m49"].map(to_iso3)
pou["value_num"] = pd.to_numeric(pou["Value"], errors="coerce")  # "<2.5" and blanks -> NaN
countries = pou[pou["iso3"].notna()]  # regions and aggregates have no ISO3 code

n_areas = pou["Area"].nunique()
n_countries = countries["Area"].nunique()
report("FAOSTAT quality assessment: Prevalence of undernourishment (%, 3-year average)")
report(f"Rows: {len(pou)} | Areas: {n_areas} ({n_countries} countries, "
       f"{n_areas - n_countries} regions or aggregates)")

report("\n== ACCURACY ==")
not_number = pou["Value"].notna() & pou["value_num"].isna()
report(f"Values that are not numbers: {not_number.sum()} "
       f"{pou.loc[not_number, 'Value'].value_counts().to_dict()}")
out_of_range = pou["value_num"].notna() & ~pou["value_num"].between(0, 100)
report(f"Numeric values outside 0-100%: {out_of_range.sum()} "
       f"(lowest {pou['value_num'].min()}, highest {pou['value_num'].max()})")
report(f"Flags: {pou['Flag'].value_counts().to_dict()} (E = estimated value, O = missing value)")

report("\n== COMPLETENESS ==")
report("Column completeness (% of rows filled in):")
for column in ["Area", "Area Code (M49)", "Year", "Unit", "Value", "Flag"]:
    report(f"  {column}: {pou[column].notna().mean() * 100:.1f}%")
missing = pou["Value"].isna()
report(f"Missing values: {missing.sum()} of {len(pou)} rows ({missing.mean() * 100:.1f}%)")
no_data = countries.groupby("Area")["Value"].apply(lambda values: values.isna().all())
report(f"Countries with no values at all: {no_data.sum()}: {'; '.join(no_data[no_data].index)}")
report(f"Countries covered: {countries['iso3'].nunique()} of "
       f"{len(pycountry.countries)} countries and territories in ISO 3166")
per_window = countries.dropna(subset=["Value"]).groupby("Year")["iso3"].nunique()
report(f"Countries with a value in each 3-year window: {per_window.min()} to {per_window.max()}")

report("\n== TIMELINESS ==")
windows = sorted(pou["Year"].unique())
report(f"3-year windows: {len(windows)}, from {windows[0]} to {windows[-1]}")

report("\n== CONSISTENCY ==")
report(f"Units used: {pou['Unit'].unique().tolist()}")
bad_format = ~pou["Year"].str.fullmatch(r"\d{4}-\d{4}")
report(f"Years not in 'YYYY-YYYY' format: {bad_format.sum()}")
span = pou["Year"].str[-4:].astype(int) - pou["Year"].str[:4].astype(int)
report(f"Windows that are not exactly 3 years long: {(span != 2).sum()}")
code_mismatch = pou["Year Code"] != pou["Year"].str.replace("-", "")
report(f"Rows where 'Year Code' does not match 'Year': {code_mismatch.sum()}")
report(f"Duplicate country-window rows: {pou.duplicated(['Area Code', 'Year']).sum()}")
apostrophe = pou["Area Code (M49)"].str.startswith("'")
report(f"M49 codes stored with a leading apostrophe (e.g. '004): {apostrophe.sum()} of {len(pou)}")
flag_matches = (pou["Value"].isna() == (pou["Flag"] == "O")).all()
report(f"Every missing value has flag O, and every flag O is missing: {flag_matches}")

REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
REPORT_FILE.write_text("\n".join(lines) + "\n")
print(f"\nSaved {REPORT_FILE.relative_to(PROJECT)}")
