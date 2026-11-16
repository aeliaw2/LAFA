import os
import pandas as pd
from country_codes import is_iso3_country

FAOSTAT = "data/cleaned/faostat_undernourishment.csv"

# name: (cleaned file path, value column)
# The SDG entry is skipped automatically until Hamza pushes his file.
# Change "mmr" to the real value column name once you see his file.
OTHERS = {
    "gdp_per_capita": ("data/cleaned/wdi_gdp_per_capita.csv", "gdp_per_capita"),
    "maternal_mortality": ("data/cleaned/sdg_maternal_mortality.csv", "mmr"),
}


def three_year_average(annual, value_col, name):
    """Average annual values over each 3-year window, keyed by the window's middle year.
    Returns iso3, year, <name>, <name>_n_years (how many of the 3 years had data, 0-3)."""
    pieces = []
    for offset in (-1, 0, 1):
        shifted = annual[["iso3", "year", value_col]].copy()
        shifted["year"] = shifted["year"] - offset  # year y feeds the window centered on y - offset
        pieces.append(shifted)
    grouped = pd.concat(pieces).groupby(["iso3", "year"])[value_col]
    return pd.DataFrame({
        name: grouped.mean(),               # blank (NaN) if no year had data
        f"{name}_n_years": grouped.count(),
    }).reset_index()


def main():
    merged = pd.read_csv(FAOSTAT)
    print(f"FAOSTAT: {len(merged)} rows, {merged['iso3'].nunique()} countries")

    for name, (path, value_col) in OTHERS.items():
        if not os.path.exists(path):
            print(f"SKIPPED {name}: {path} not found yet")
            continue

        annual = pd.read_csv(path)

        # Sanity checks
        dupes = annual.duplicated(["iso3", "year"]).sum()
        print(f"{name}: {len(annual)} annual rows, {annual['iso3'].nunique()} countries, "
              f"{dupes} duplicate country-year rows")
        not_iso3 = sorted(c for c in annual["iso3"].unique() if not is_iso3_country(c))
        print(f"{name}: codes not in pycountry (check these): {not_iso3}")

        # Countries that don't match across datasets
        fao, other = set(merged["iso3"]), set(annual["iso3"])
        print(f"{name}: in FAOSTAT only ({len(fao - other)}): {sorted(fao - other)}")
        print(f"{name}: in {name} only ({len(other - fao)}): {sorted(other - fao)}")

        # 3-year average + n_years, then left join onto FAOSTAT's country-window rows
        avg = three_year_average(annual, value_col, name)
        merged = merged.merge(avg, on=["iso3", "year"], how="left")
        merged[f"{name}_n_years"] = merged[f"{name}_n_years"].fillna(0).astype(int)

        print(f"{name}: rows by number of years averaged:")
        print(merged[f"{name}_n_years"].value_counts().sort_index())

    os.makedirs("data/integrated", exist_ok=True)
    merged.to_csv("data/integrated/integrated.csv", index=False)
    print(f"\nWrote data/integrated/integrated.csv: {len(merged)} rows")
    print("Percent missing per column:")
    print((merged.isna().mean() * 100).round(1))


if __name__ == "__main__":
    main()