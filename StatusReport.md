
# Status Report

**Economic Development, Food Insecurity, and Maternal Mortality Across Countries**

**Team:** Abigail Liaw, Hamza Ahmed, Olusegun Fajinmi, Shannon Ahn

---

## 1. Progress on Project Tasks

### 1.1 Data Acquisition

#### FAOSTAT – Prevalence of Undernourishment (Abigail)

[`scripts/acquire_faostat.py`](scripts/acquire_faostat.py) downloads FAOSTAT's bulk file for the Suite of Food Security Indicators domain into [`data/raw/`](data/raw/) and verifies it with a SHA-256 checksum.

The first run saved the checksum to [`data/raw/faostat_food_security.zip.sha256`](data/raw/faostat_food_security.zip.sha256), and every later run stops with an error if the file has changed.

**Status:** Complete

#### UN SDG – Maternal Mortality Ratio (Hamza)

Our original UN SDG dataset only included internal UN geographic codes without country names, which made it difficult to match countries across datasets. To address this, we re-downloaded the maternal mortality dataset from the United Nations Global SDG Database with standard country identifiers and names.

The acquisition script, [`scripts/acquire_sdg.py`](scripts/acquire_sdg.py), is intended to automate the download and use a SHA-256 checksum to verify the file's integrity. The dataset will be stored in [`data/raw/sdg_maternal_mortality.csv`](data/raw/sdg_maternal_mortality.csv) so it can be used for the remaining data quality and cleaning steps.

**Status:** In progress

#### World Bank WDI – GDP per Capita (Olusegun)

Using [`scripts/acquire_wdi.py`](scripts/acquire_wdi.py), we downloaded GDP per capita (current US$, indicator `NY.GDP.PCAP.CD`) for 2000 to 2025 from the World Bank API into [`data/raw/wdi_gdp_per_capita.json`](data/raw/wdi_gdp_per_capita.json). It also downloads the World Bank's country list into [`data/raw/wdi_countries.json`](data/raw/wdi_countries.json), which we use to tell countries apart from regional groups.

The first run saved a SHA-256 checksum for each file in `data/raw/` (`wdi_gdp_per_capita.json.sha256` and `wdi_countries.json.sha256`), and every later run stops with an error if a file has changed.

**Status:** Complete

### 1.2 Pre-Integration Data Quality Assessment

#### FAOSTAT (Abigail)

[`scripts/assess_faostat.py`](scripts/assess_faostat.py) checks the 5,904 undernourishment rows and saves its results to [`reports/faostat_quality.txt`](reports/faostat_quality.txt).

- **Accuracy:** All numeric values fall between 2.5% and 72.5%, but 1,452 values are the text `<2.5` (below 2.5%) rather than numbers, and all values are FAO estimates (flag E).
- **Completeness:** 14.9% of values are missing; 203 of the 246 areas are countries (the rest are regions or aggregates); 34 countries, mostly small island states, have no values at all; and 166–168 countries have a value in each window.
- **Timeliness:** 24 three-year windows, from 2000–2002 to 2023–2025.
- **Consistency:** One unit (%), every year is in `YYYY-YYYY` format and spans exactly three years, there are no duplicate rows, and every missing value has flag O. Every M49 code is stored with a leading apostrophe (`'004`), which cleaning removes.

#### UN SDG (Hamza)

Our pre-integration quality assessment focuses on four dimensions: accuracy, completeness, timeliness, and consistency. For accuracy, we will check that maternal mortality ratios are numeric, nonnegative, and measured in deaths per 100,000 live births. For completeness, we will examine missing values and count how many countries have available data. For timeliness, we identified that the dataset ends in 2020, which limits its overlap with the more recent FAOSTAT observations. For consistency, we will check for duplicate country-year records and verify that country identifiers and year formats are standardized. These checks will help us identify issues before combining the UN SDG data with the other datasets.

#### World Bank WDI (Olusegun)

[`scripts/assess_wdi.py`](scripts/assess_wdi.py) checks the 6,916 rows of GDP per capita and saves its results to [`reports/wdi_quality.txt`](reports/wdi_quality.txt).

- **Accuracy:** Values range from $109.59 to $288,001.57, there are no zero or negative values, and all values are numeric.
- **Completeness:** 3.8% of country values are missing, 3 countries have no values at all, and 186 to 214 countries have a value in each year. The file also includes 44 regional and income groups (such as "World" and "High income") that are not countries.
- **Timeliness:** Years run from 2000 to 2025, and 186 countries have a value in the latest year.
- **Consistency:** One unit (current US$), every year is a four-digit number, and there are no duplicate country-year rows. 130 rows have no ISO3 code.

### 1.3 Data Cleaning

#### FAOSTAT (Abigail)

[`scripts/clean_faostat.py`](scripts/clean_faostat.py) produces [`data/cleaned/faostat_undernourishment.csv`](data/cleaned/faostat_undernourishment.csv) (4,872 rows: 203 countries × 24 windows).

Each step addresses an issue from the quality assessment:

1. **Leading apostrophes in M49 codes:** Removed, then codes converted to ISO3 with `pycountry` so they match the other datasets.
2. **Regions mixed with countries:** The 43 areas with no ISO3 code (regions and aggregates, including FAOSTAT's combined "China") are dropped. "China, mainland" is kept as CHN.
3. **3-year windows instead of single years:** Each window keeps its original label (`window`) and gets its middle year (`year`, for example 2009–2011 → 2010) for joining.
4. **`<2.5` text values (1,205 country rows):** Stored as 2.5 with a `below_2_5` flag column, since FAO reports these as below 2.5%. Leaving them blank would have removed mostly high-income, low-hunger countries from the analysis.
5. **Missing values (858 country rows):** Left blank, not filled in.

#### UN SDG (Hamza)

Our data cleaning process focuses on preparing the maternal mortality dataset for integration with the World Bank and FAOSTAT data. The main issue identified was that our original file used internal UN country codes, which could not be directly matched with the other sources. We addressed this by obtaining a new version containing standard country identifiers and names. The planned cleaning script, [`scripts/clean_sdg.py`](scripts/clean_sdg.py), will select the columns needed for our analysis, standardize country codes into ISO3 format, and make sure years and mortality values are stored consistently. We will also remove regional aggregates and preserve missing values rather than filling them with assumptions. These steps will help create a consistent country-year dataset that can be merged with the other sources.

The cleaned output is planned for `data/cleaned/sdg_maternal_mortality.csv`.

#### World Bank WDI (Olusegun)

[`scripts/clean_wdi.py`](scripts/clean_wdi.py) produces [`data/cleaned/wdi_gdp_per_capita.csv`](data/cleaned/wdi_gdp_per_capita.csv) (5,642 rows: 217 countries × 26 years).

Each step addresses an issue from the quality assessment:

1. **Regional and income groups mixed with countries:** The 44 groups the World Bank labels "Aggregates" (1,144 rows) are dropped, so only countries remain.
2. **Rows with no ISO3 code:** The 130 rows with no code are dropped, since they can't be matched to the other datasets.
3. **Years stored as text:** Converted to whole numbers so they join with the other datasets.
4. **Missing values (214 country rows):** Left blank, not filled in.

### 1.4 Data Integration (Shannon)

**Country-code helper**
[`scripts/country_codes.py`](scripts/country_codes.py) uses `pycountry` to convert M49 codes and country names to ISO3, with a manual rule for China (FAOSTAT's combined "China" is excluded and "China, mainland" maps to CHN). It also checks whether a code is a real country code, which we use to flag unrecognized codes during integration.

**Year matching**
[`scripts/integrate.py`](scripts/integrate.py) starts from FAOSTAT's 4,872 country-window rows. For GDP per capita, it averages the annual values over the three years of each window and records a `gdp_per_capita_n_years` column (0–3) for how many years had data. Missing values stay blank.

**Merge and results**

The cleaned WDI file is left-joined to FAOSTAT on `iso3` and `year`, so FAOSTAT defines the country-window grid and the row count stays at 4,872. Four FAOSTAT countries have no WDI data (Cook Islands, Niue, Tokelau, Taiwan), and 18 WDI countries and territories are not in FAOSTAT (mostly small territories, plus Kosovo, which `pycountry` does not recognize). In the output, 4,691 rows (96.3%) average all three years, 25 rows average one or two years, and 156 rows (3.2%) have no GDP value. 17.6% of rows have no undernourishment value. The result is saved to [`data/integrated/integrated.csv`](data/integrated/integrated.csv).

**Status: In progress.** FAOSTAT and WDI are merged. The maternal mortality data will be added once the cleaned UN SDG file is available, after which we will rerun `integrate.py`, review unmatched countries, and run the post-integration quality check.

### 1.5 Workflow and Reproducibility

The whole workflow runs with one command from the project root: `bash run_all.sh`. It installs the packages in [`requirements.txt`](requirements.txt), then runs each dataset's scripts in order (acquire, assess, clean). Every script uses relative paths, so it runs without edits.

Folder structure:

- [`data/raw/`](data/raw/) holds the original downloads and their `.sha256` checksum files.
- [`data/cleaned/`](data/cleaned/) holds one cleaned CSV per dataset.
- [`scripts/`](scripts/) holds one script per step.
- [`reports/`](reports/) holds the quality-check output.
- [`run_all.sh`](run_all.sh), [`requirements.txt`](requirements.txt), README, [`ProjectPlan.md`](ProjectPlan.md) and `StatusReport.md` sit in the project root.

### 1.6 Post-Integration Data Quality Assessment

Planned for after the midterm (see timeline). It will repeat the four-dimension assessment on the integrated table.

---

## 2. Updated Timeline

| Task | Owner | Original Dates | Status | Expected Completion |
|---|---|---|---|---|
| Setup and acquisition | Abigail, Hamza, Olusegun | Oct 12–21 | Done | Nov 15 |
| Pre-integration quality assessment | Abigail, Hamza, Olusegun | Oct 19–Nov 1 | Done | Nov 15 |
| Data cleaning | Abigail, Hamza, Olusegun | Oct 26–Nov 8 | Done | Nov 15 |
| Country-code helper and integration | Shannon | Nov 2–12 | Done | Nov 15 |
| Post-integration quality assessment | Shannon | Nov 9–17 | Not started | After Nov 20 |
| Interim status report | Everyone | Nov 10–19 | Done | Nov 16 |
| Analysis and visualization | TBD | Nov 18–28 | Not started | Nov 28 |
| Workflow, metadata, and documentation | Olusegun | Nov 20–Dec 3 | In progress | Dec 3 |
| Final README and GitHub release | TBD | Dec 1–7 | Not started | Dec 7 |

---

## 3. Changes to the Project Plan

### 3.1 Changes Based on Milestone 2 Feedback

Our feedback asked us to address "matching year values to 3-year averages, and tracking what data is missing." We made both concrete:

#### Year Matching

Each FAOSTAT 3-year window is labeled with its middle year (for example, 2009–2011 becomes 2010).

For GDP per capita and maternal mortality, we average the annual values for the same three years and add an `n_years` column recording how many years had data.

This makes gaps visible: the SDG data ends in 2020, so the 2019–2021 window has at most two years of maternal mortality data.

#### Tracking Missing Data

Missing values are left blank, not filled in.

Each quality-check script reports the percentage missing per column and the number of countries covered.

The integration step uses an outer merge to count and list countries that do not match across datasets.

FAOSTAT values reported as `<2.5` (below 2.5%) are kept separate from truly missing values with a flag column.

### 3.2 Other Changes

- **Dropped Variables:** We removed life expectancy and total population because our research questions do not use them.
- **FAOSTAT Source:** We replaced the manual web export with a scripted download of FAOSTAT's bulk file, so acquisition is reproducible.
- **WDI Source:** We download only GDP per capita from the World Bank instead of the full 198 MB WDI file. This keeps the data under GitHub's 50 MB limit, so Box is not needed.
- **UN SDG Source:** Our original file identified countries only by internal UN codes (for example, `G00000020`) with no country names, so we re-downloaded a version with standard country codes and names.
- **Country Codes:** We convert M49 codes to ISO3 with the `pycountry` library. Every area that does not convert is a region or aggregate (including FAOSTAT's "China," which combines mainland China, Hong Kong, Macao and Taiwan), so dropping them removes the regional groups our plan said to exclude.
- **Tools:** Cleaning is done in Python with pandas, and the workflow is run by a single run-all script.
- **Schedule:** The status report deadline moved to November 16 and the midterm is November 17–20, so the post-integration quality assessment moved to after the midterm.
- **Roles:** Each of Abigail, Hamza and Olusegun now owns one dataset from acquisition through cleaning, and Shannon owns country codes and integration.
- **Updated Plan:** In [`ProjectPlan.md`](ProjectPlan.md), we revised the integration, data quality and cleaning sections (5–7) to address the feedback, and updated the dataset descriptions (Section 4) to match the new sources and files.

---

## 4. Challenges and Resolutions

### 4.1 UN SDG Country Codes

**Challenge:** Our original UN SDG dataset used internal geographic codes without country names, making it difficult to match the data with our other datasets.

**Resolution:** We re-downloaded the dataset with standard country identifiers and names. This allows us to standardize the countries using ISO3 codes and makes integration more manageable.

### 4.2 World Bank WDI File Size

**Challenge:** The original World Bank dataset was approximately 198 MB, which exceeded the GitHub file size limit outlined in our project requirements.

**Resolution:** Instead of downloading the entire dataset, we decided to download only the GDP per capita indicator. This reduces the file size while still providing the information needed for our research questions.

### 4.3 Non-Numeric FAOSTAT Values

**Challenge:** Some FAOSTAT undernourishment values were reported as text, such as (<2.5), rather than numbers. This creates problems when performing calculations and combining datasets.

**Resolution:** We stored these values as 2.5 and added a flag column to indicate that the original observation was below 2.5%. This allows us to use the data while keeping track of how the values were originally reported.

### 4.4 Differences in Year Coverage

**Challenge:** The three datasets do not cover exactly the same years. The UN SDG maternal mortality data ends in 2020, while FAOSTAT includes three-year reporting periods through 2023–2025.

**Resolution:** We decided to align the datasets using FAOSTAT's three-year windows and calculate averages for the corresponding annual observations. We will also use an n_years column to track how many years of data are available, allowing us to identify incomplete periods.

### 4.5 Inconsistent China Definitions

**Challenge:** FAOSTAT includes a combined China category that covers mainland China, Hong Kong, Macao, and Taiwan, while the other datasets identify mainland China separately.

**Resolution:** We decided to use FAOSTAT's "China, mainland" entry and exclude the combined category. This helps prevent inconsistencies when matching countries across the datasets.

### 4.6 Schedule Changes

**Challenge:** The status report deadline was moved earlier to November 16, which also overlaps with our midterm exam period. This gives our team less time to finish certain parts of the project.

**Resolution:** We adjusted our schedule and prioritized data acquisition, cleaning, and the status report. We also moved the post-integration data quality assessment until after the midterm period so we can complete the remaining work without rushing the earlier steps.

---

## 5. Individual Contributions

### 5.1 Abigail Liaw

I handled the FAOSTAT dataset from downloading it to cleaning it. I wrote and ran scripts to download the bulk Food Security file, verify it with a SHA-256 checksum, and check its accuracy, completeness, timeliness, and consistency. I also wrote the cleaning script to convert country codes to ISO3, remove regional aggregates, label each three-year window with its middle year, and flag values reported as "<2.5".

For Milestone 3, I organized the task split and timeline and narrowed the project scope after reviewing the course materials. I also updated the dataset descriptions in ProjectPlan.md to reflect our new sources, wrote the "Changes to the Project Plan" section, and put together this status report.

### 5.2 Hamza Ahmed

For Milestone 3, I focused on the UN SDG maternal mortality dataset and helped address issues with the original country's geographic identifiers by identifying a version with standard country codes and names. I also worked on planning the data quality assessment and cleaning steps needed to prepare the dataset for integration. Additionally, I documented the main challenges our team encountered and explained how we resolved them or plan to address them moving forward.

### 5.3 Olusegun Fajinmi

I took the World Bank GDP per capita data from start to finish. I wrote the scripts that download it, check it with a SHA-256 checksum, look at its quality, and take out the regional and income groups. I also put together the run-all script and the requirements file. In the project plan, I wrote the ethical and legal, workflow, and timeline sections, and for this report I filled in the updated timeline.

### 5.4 Shannon Ahn

I wrote the country-code helper (`country_codes.py`), which converts identifiers to ISO3 with `pycountry` and includes a manual rule for China. I wrote `integrate.py`, which averages GDP per capita over each FAOSTAT 3-year window, adds an `n_years` column to track missing data, and left-joins the result onto the FAOSTAT table to produce `data/integrated/integrated.csv`. The maternal mortality data will be added once the cleaned SDG file is available.

