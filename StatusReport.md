
# Status Report

**Economic Development, Food Insecurity, and Maternal Mortality Across Countries**

**Team:** Abigail Liaw, Hamza Ahmed, Olusegun Fajinmi, Shannon Ahn

---

## 1. Progress on Project Tasks

### 1.1 Data Acquisition

Each script downloads its dataset into [`data/raw/`](data/raw/), saves a SHA-256 checksum on the first run, and stops with an error later if the file changes.

- **FAOSTAT (Abigail), complete:** [`scripts/acquire_faostat.py`](scripts/acquire_faostat.py) downloads FAOSTAT's bulk Food Security file ([`faostat_food_security.zip`](data/raw/faostat_food_security.zip)).
- **World Bank WDI (Olusegun), complete:** [`scripts/acquire_wdi.py`](scripts/acquire_wdi.py) downloads GDP per capita (`NY.GDP.PCAP.CD`, 2000–2025) from the World Bank API, plus the country list used to separate countries from regional groups ([`wdi_gdp_per_capita.json`](data/raw/wdi_gdp_per_capita.json), [`wdi_countries.json`](data/raw/wdi_countries.json)).
- **UN SDG (Hamza), in progress:** our original file identified countries only by internal UN codes, so we re-downloaded the maternal mortality ratio from the UN Global SDG Database with standard country codes and names. The script that automates this download and its checksum (`scripts/acquire_sdg.py`, saving `data/raw/sdg_maternal_mortality.csv`) is in progress.

### 1.2 Pre-Integration Data Quality Assessment

**FAOSTAT (Abigail):** [`scripts/assess_faostat.py`](scripts/assess_faostat.py) checks the 5,904 undernourishment rows and saves [`reports/faostat_quality.txt`](reports/faostat_quality.txt).

- **Accuracy:** numeric values range from 2.5% to 72.5%, but 1,452 values are the text `<2.5`; all values are FAO estimates.
- **Completeness:** 14.9% of values are missing; 203 of 246 areas are countries; 34 countries have no values at all.
- **Timeliness:** 24 three-year windows, from 2000–2002 to 2023–2025.
- **Consistency:** one unit, consistent `YYYY-YYYY` years, no duplicates; every M49 code has a leading apostrophe (`'004`).

**World Bank WDI (Olusegun):** [`scripts/assess_wdi.py`](scripts/assess_wdi.py) checks the 6,916 rows and saves [`reports/wdi_quality.txt`](reports/wdi_quality.txt).

- **Accuracy:** all values are numeric and positive ($109.59 to $288,001.57).
- **Completeness:** 3.8% of country values are missing; 3 countries have no values; 44 entries are regional or income groups, not countries.
- **Timeliness:** 2000–2025; 186 countries have a value in the latest year.
- **Consistency:** one unit, four-digit years, no duplicates; 130 rows have no ISO3 code.

**UN SDG (Hamza):** in progress, covering the same four dimensions. The data end in 2020, which limits overlap with FAOSTAT's later windows.

### 1.3 Data Cleaning

**FAOSTAT (Abigail):** [`scripts/clean_faostat.py`](scripts/clean_faostat.py) produces [`data/cleaned/faostat_undernourishment.csv`](data/cleaned/faostat_undernourishment.csv) (203 countries × 24 windows = 4,872 rows). Each step fixes an issue found in the assessment:

- Removes the apostrophes and converts M49 codes to ISO3 with `pycountry`.
- Drops the 43 regions and aggregates, including FAOSTAT's combined "China"; "China, mainland" becomes CHN.
- Labels each window with its middle year (2009–2011 → 2010).
- Stores `<2.5` as 2.5 with a `below_2_5` flag (1,205 rows), so low-hunger countries are not lost.
- Leaves the 858 missing values blank.

**World Bank WDI (Olusegun):** [`scripts/clean_wdi.py`](scripts/clean_wdi.py) produces [`data/cleaned/wdi_gdp_per_capita.csv`](data/cleaned/wdi_gdp_per_capita.csv) (217 countries × 26 years = 5,642 rows). It drops the 44 World Bank "Aggregates" (1,144 rows) and the 130 rows with no ISO3 code, converts years from text to numbers, and leaves 214 missing values blank.

**UN SDG (Hamza):** the planned `scripts/clean_sdg.py` will keep the needed columns, convert country codes to ISO3, remove regional aggregates, and leave missing values blank, saving `data/cleaned/sdg_maternal_mortality.csv`.

### 1.4 Data Integration (Shannon)

**Status:** in progress. FAOSTAT and WDI are merged; maternal mortality will be added once the cleaned SDG file is ready.

[`scripts/country_codes.py`](scripts/country_codes.py) converts M49 codes and country names to ISO3 with `pycountry` and flags unrecognized codes. [`scripts/integrate.py`](scripts/integrate.py) starts from FAOSTAT's 4,872 country-window rows, averages GDP per capita over each window's three years, and records how many years had data (`gdp_per_capita_n_years`, 0–3). The WDI data are left-joined on `iso3` and `year`, so FAOSTAT defines the grid, and the result is saved to [`data/integrated/integrated.csv`](data/integrated/integrated.csv).

Results so far:

- 4,691 rows (96.3%) average all three years of GDP, 25 average one or two, and 156 (3.2%) have none.
- Four FAOSTAT countries have no WDI data (Cook Islands, Niue, Tokelau, Taiwan), and 18 WDI countries and territories are not in FAOSTAT (mostly small territories, plus Kosovo).

### 1.5 Workflow and Reproducibility

[`run_all.sh`](run_all.sh) runs the workflow from the project root (`bash run_all.sh`): it installs [`requirements.txt`](requirements.txt), then runs each dataset's acquire, assess, and clean scripts in order, using relative paths. Data are stored in [`data/raw/`](data/raw/), [`data/cleaned/`](data/cleaned/) and [`data/integrated/`](data/integrated/), scripts in [`scripts/`](scripts/), and quality reports in [`reports/`](reports/).

### 1.6 Post-Integration Data Quality Assessment

Planned for after the midterm, once maternal mortality is integrated.

---

## 2. Updated Timeline

| Task | Owner | Original Dates | Status | Expected Completion |
|---|---|---|---|---|
| Setup and acquisition | Abigail, Hamza, Olusegun | Oct 12–21 | FAOSTAT, WDI done; SDG in progress | After Nov 20 |
| Pre-integration quality assessment | Abigail, Hamza, Olusegun | Oct 19–Nov 1 | FAOSTAT, WDI done; SDG in progress | After Nov 20 |
| Data cleaning | Abigail, Hamza, Olusegun | Oct 26–Nov 8 | FAOSTAT, WDI done; SDG in progress | After Nov 20 |
| Country-code helper and integration | Shannon | Nov 2–12 | In progress (FAOSTAT and WDI merged) | After Nov 20 |
| Post-integration quality assessment | Shannon | Nov 9–17 | Not started | After Nov 20 |
| Interim status report | Everyone | Nov 10–19 | Done | Nov 16 |
| Analysis and visualization | TBD | Nov 18–28 | Not started | Nov 28 |
| Workflow, metadata, and documentation | Olusegun | Nov 20–Dec 3 | In progress | Dec 3 |
| Final README and GitHub release | TBD | Dec 1–7 | Not started | Dec 7 |

---

## 3. Changes to the Project Plan

### 3.1 Based on Milestone 2 Feedback

Our feedback asked us to address "matching year values to 3-year averages, and tracking what data is missing."

- **Year matching:** each FAOSTAT window is labeled with its middle year, and annual GDP per capita and maternal mortality are averaged over the same three years, with an `n_years` column recording how many years had data. This makes gaps visible: the SDG data end in 2020, so the 2019–2021 window has at most two years of data.
- **Missing data:** missing values are left blank, not filled in. Each quality-check script reports missing values and country coverage, the integration step lists countries that do not match across datasets, and FAOSTAT's `<2.5` values are flagged separately from truly missing values.

### 3.2 Other Changes

- **Variables:** we dropped life expectancy and total population, which our research questions do not use.
- **Sources:** FAOSTAT is now a scripted bulk download instead of a manual export, WDI downloads only GDP per capita, and the UN SDG data were re-downloaded with standard country codes (see Section 4).
- **Roles:** Abigail, Hamza and Olusegun each own one dataset through cleaning, and Shannon owns country codes and integration.
- **Plan updates:** [`ProjectPlan.md`](ProjectPlan.md) Sections 5–7 were revised to address the feedback, and Section 4 was updated for the new sources.

---

## 4. Challenges and Resolutions

- **SDG country codes:** the original file had internal UN codes and no country names. *Resolution:* we re-downloaded it with standard codes and names.
- **WDI file size:** the full WDI file (198 MB) exceeded GitHub's limit. *Resolution:* we download only GDP per capita.
- **Non-numeric FAOSTAT values:** 1,452 values were the text `<2.5`. *Resolution:* they are stored as 2.5 with a flag column.
- **China definitions:** FAOSTAT's "China" combines mainland China, Hong Kong, Macao and Taiwan. *Resolution:* we use "China, mainland" and drop the combined area.
- **Different year coverage and unmatched countries:** see Sections 3.1 and 1.4. Unmatched countries are kept with blank values and will be reviewed once maternal mortality is added.
- **Earlier deadline:** the report deadline moved to midterm week. *Resolution:* we prioritized acquisition, cleaning and this report, and moved post-integration quality assessment to after the midterm.

---

## 5. Individual Contributions

### 5.1 Abigail Liaw

I handled the FAOSTAT dataset from download to cleaning, writing and running its acquisition, quality-assessment, and cleaning scripts. I also organized the Milestone 3 task split and timeline, narrowed the project scope after reviewing the course materials, updated the dataset descriptions in ProjectPlan.md, wrote the "Changes to the Project Plan" section, and assembled this report.

### 5.2 Hamza Ahmed

For Milestone 3, I focused on the UN SDG maternal mortality dataset and helped address issues with the original country's geographic identifiers by identifying a version with standard country codes and names. I also worked on planning the data quality assessment and cleaning steps needed to prepare the dataset for integration. Additionally, I documented the main challenges our team encountered and explained how we resolved them or plan to address them moving forward.

### 5.3 Olusegun Fajinmi

I took the World Bank GDP per capita data from start to finish. I wrote the scripts that download it, check it with a SHA-256 checksum, look at its quality, and take out the regional and income groups. I also put together the run-all script and the requirements file. In the project plan, I wrote the ethical and legal, workflow, and timeline sections, and for this report I filled in the updated timeline.

### 5.4 Shannon Ahn

I wrote the country-code helper (country_codes.py), which converts identifiers to ISO3 with pycountry and includes a manual rule for China. I wrote integrate.py, which averages GDP per capita over each FAOSTAT 3-year window, adds an n_years column to track missing data, and left-joins the result onto the FAOSTAT table to produce data/integrated/integrated.csv. The maternal mortality data will be added once the cleaned SDG file is available.


