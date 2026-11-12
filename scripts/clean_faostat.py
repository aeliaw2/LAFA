"""Workflow step: clean the FAOSTAT undernourishment data.

Run from the project folder:  python scripts/clean_faostat.py

Input:  data/raw/faostat_food_security.zip (raw FAOSTAT bulk file)
Output: data/cleaned/faostat_undernourishment.csv, one row per country and 3-year window,
        with columns: iso3, country, window, year, undernourishment_pct, below_2_5

Each step fixes an issue found in the quality assessment (reports/faostat_quality.txt).
"""
import zipfile
from pathlib import Path

import pandas as pd
import pycountry

PROJECT = Path(__file__).resolve().parent.parent
RAW_FILE = PROJECT / "data" / "raw" / "faostat_food_security.zip"
CLEAN_FILE = PROJECT / "data" / "cleaned" / "faostat_undernourishment.csv"
DATA_CSV = "Food_Security_Data_E_All_Data_(Normalized).csv"  # main data file inside the zip
POU_ITEM_CODE = "210041"  # Prevalence of undernourishment (percent) (3-year average)


def to_iso3(m49_code):
    """Convert an M49 country code like '004' to ISO3 like 'AFG'. Regions return None."""
    country = pycountry.countries.get(numeric=m49_code)
    return country.alpha_3 if country else None


# 1. Load the raw data as text and keep only the undernourishment rows
with zipfile.ZipFile(RAW_FILE) as archive:
    df = pd.read_csv(archive.open(DATA_CSV), dtype=str)
df = df[(df["Item Code"] == POU_ITEM_CODE) & (df["Element"] == "Value")].copy()
print(f"Undernourishment rows: {len(df)}")

# 2. Country codes: remove the leading apostrophe ("'004" -> "004"), then convert to ISO3
df["iso3"] = df["Area Code (M49)"].str.lstrip("'").map(to_iso3)

# 3. Drop regions and aggregates (they have no ISO3 code). This also drops FAOSTAT's
#    "China" (mainland + Hong Kong + Macao + Taiwan); "China, mainland" is kept as CHN.
n_dropped = df.loc[df["iso3"].isna(), "Area"].nunique()
df = df[df["iso3"].notna()].copy()
print(f"Dropped {n_dropped} regions/aggregates, kept {df['iso3'].nunique()} countries")

# 4. Years: label each 3-year window with its middle year ("2009-2011" -> 2010)
df["window"] = df["Year"]
df["year"] = df["Year"].str[:4].astype(int) + 1

# 5. Values: "<2.5" means below 2.5%. Store it as 2.5 and flag it, so it can be
#    told apart from exact values. Missing values stay blank (not filled in).
df["below_2_5"] = df["Value"] == "<2.5"
df["undernourishment_pct"] = pd.to_numeric(df["Value"].replace("<2.5", "2.5"))

# 6. Keep only the columns we need, with clear names, and save
clean = df.rename(columns={"Area": "country"})
clean = clean[["iso3", "country", "window", "year", "undernourishment_pct", "below_2_5"]]
clean = clean.sort_values(["iso3", "year"])

# Quick checks that cleaning worked
assert not clean.duplicated(["iso3", "year"]).any(), "duplicate country-year rows"
assert clean["undernourishment_pct"].dropna().between(0, 100).all(), "value outside 0-100%"

CLEAN_FILE.parent.mkdir(parents=True, exist_ok=True)
clean.to_csv(CLEAN_FILE, index=False)
print(f"Saved {CLEAN_FILE.relative_to(PROJECT)}: {len(clean)} rows, "
      f"{clean['iso3'].nunique()} countries, years {clean['year'].min()}-{clean['year'].max()}")
print(f"  Missing values (left blank): {clean['undernourishment_pct'].isna().sum()}")
print(f"  Values below 2.5% (stored as 2.5, flagged): {clean['below_2_5'].sum()}")
