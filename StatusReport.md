
# Status Report

**Economic Development, Food Insecurity, and Maternal Mortality Across Countries**

**Team:** Abigail Liaw, Hamza Ahmed, Olusegun Fajinmi, Shannon Ahn

> **TODO – Everyone:** Write in your own section and commit it from your own account. The whole report should be about 1,000–1,500 words. Delete every TODO note before we tag the release.

---

## 1. Progress on Project Tasks

### 1.1 Data Acquisition

#### FAOSTAT – Prevalence of Undernourishment (Abigail)

`scripts/acquire_faostat.py` downloads FAOSTAT's bulk file for the Suite of Food Security Indicators domain into `data/raw/` and verifies it with a SHA-256 checksum.

The first run saved the checksum to `data/raw/faostat_food_security.zip.sha256`, and every later run stops with an error if the file has changed.

**Status:** Complete

#### UN SDG – Maternal Mortality Ratio (Hamza)

> **TODO – Hamza:** What your script downloads, from where, how it checks the SHA-256, and the script and data file paths.

#### World Bank WDI – GDP per Capita (Olusegun)

> **TODO – Olusegun:** Same as above.

### 1.2 Pre-Integration Data Quality Assessment

#### FAOSTAT (Abigail)

`scripts/assess_faostat.py` checks the 5,904 undernourishment rows and saves its results to `reports/faostat_quality.txt`.

- **Accuracy:** All numeric values fall between 2.5% and 72.5%, but 1,452 values are the text `<2.5` (below 2.5%) rather than numbers, and all values are FAO estimates (flag E).

- **Completeness:** 14.9% of values are missing; 203 of the 246 areas are countries (the rest are regions or aggregates); 34 countries, mostly small island states, have no values at all; and 166–168 countries have a value in each window.

- **Timeliness:** 24 three-year windows, from 2000–2002 to 2023–2025.

- **Consistency:** One unit (%), every year is in `YYYY-YYYY` format and spans exactly three years, there are no duplicate rows, and every missing value has flag O. Every M49 code is stored with a leading apostrophe (`'004`), which cleaning removes.

> **TODO – Hamza, Olusegun:** One short paragraph each covering accuracy, completeness, timeliness, and consistency, with the main numbers and the quality-check script and output file paths in `reports/`.

### 1.3 Data Cleaning

#### FAOSTAT (Abigail)

`scripts/clean_faostat.py` produces `data/cleaned/faostat_undernourishment.csv` (4,872 rows: 203 countries × 24 windows).

Each step addresses an issue from the quality assessment:

1. **Leading apostrophes in M49 codes:** Removed, then codes converted to ISO3 with `pycountry` so they match the other datasets.

2. **Regions mixed with countries:** The 43 areas with no ISO3 code (regions and aggregates, including FAOSTAT's combined "China") are dropped. "China, mainland" is kept as CHN.

3. **3-year windows instead of single years:** Each window keeps its original label (`window`) and gets its middle year (`year`, for example 2009–2011 → 2010) for joining.

4. **`<2.5` text values (1,205 country rows):** Stored as 2.5 with a `below_2_5` flag column, since FAO reports these as below 2.5%. Leaving them blank would have removed mostly high-income, low-hunger countries from the analysis.

5. **Missing values (858 country rows):** Left blank, not filled in.

> **TODO – Hamza, Olusegun:** What your cleaning script does and which quality problem each step fixes. Include the script and cleaned file paths in `data/cleaned/`.

### 1.4 Data Integration

> **TODO – Shannon:** Country-code helper, how the 3-year windows are matched, and status of the integration script, with file paths.

### 1.5 Workflow and Reproducibility

> **TODO – Olusegun:** Folder structure, run-all script, and `requirements.txt`, with file paths.

### 1.6 Post-Integration Data Quality Assessment

Planned for after the midterm (see timeline). It will repeat the four-dimension assessment on the integrated table.

---

## 2. Updated Timeline

> **TODO – Olusegun:** Fill in Status (Done / In progress / Not started) and Expected completion.

| Task | Owner | Original Dates | Status | Expected Completion |
|---|---|---|---|---|
| Setup and acquisition | Abigail, Hamza, Olusegun | Oct 12–21 | | |
| Pre-integration quality assessment | Abigail, Hamza, Olusegun | Oct 19–Nov 1 | | |
| Data cleaning | Abigail, Hamza, Olusegun | Oct 26–Nov 8 | | |
| Country-code helper and integration | Shannon | Nov 2–12 | | |
| Post-integration quality assessment | Shannon | Nov 9–17 | | |
| Interim status report | Everyone | Nov 10–19 | | |
| Analysis and visualization | | Nov 18–28 | | |
| Workflow, metadata, and documentation | Olusegun | Nov 20–Dec 3 | | |
| Final README and GitHub release | | Dec 1–7 | | |

---

## 3. Changes to the Project Plan

> **TODO – Abigail:** Draft below. Check that each change actually happened before submitting.

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

- **Updated Plan:** In `ProjectPlan.md`, we revised the integration, data quality and cleaning sections (5–7) to address the feedback, and updated the dataset descriptions (Section 4) to match the new sources and files.

---

## 4. Challenges and Resolutions

> **TODO – Hamza:** For each challenge, say how we resolved it or how we plan to.

### 4.1 UN SDG Country Codes

**Challenge:** The SDG file used internal UN codes with no country names.

**Resolution:** Re-downloaded the file with standard country codes and names.

### 4.2 World Bank WDI File Size

**Challenge:** The full WDI file was 198 MB, over GitHub's limit.

**Resolution:** Download GDP per capita only.

### 4.3 Non-Numeric FAOSTAT Values

**Challenge:** FAOSTAT reports some values as text (`<2.5`) instead of numbers.

**Resolution:** Use a flag column to distinguish these values.

### 4.4 Differences in Year Coverage

**Challenge:** The years only partly overlap. SDG ends in 2020 and FAOSTAT runs from 2000–2002 to 2023–2025, so the shared windows end at 2019–2021.

**Resolution:** Use an `n_years` column to track how many annual observations are available.

### 4.5 Inconsistent China Definitions

**Challenge:** FAOSTAT's "China" combines mainland China, Hong Kong, Macao and Taiwan, while the other datasets use mainland China.

**Resolution:** Use FAOSTAT's "China, mainland" entry.

### 4.6 Schedule Changes

**Challenge:** The status report deadline moved earlier, during midterm week.

**Resolution:** Reprioritized tasks.

---

## 5. Individual Contributions

### 5.1 Abigail Liaw

I handled the FAOSTAT dataset from downloading it to cleaning it. I wrote and ran scripts to download the bulk Food Security file, verify it with a SHA-256 checksum, and check its accuracy, completeness, timeliness, and consistency. I also wrote the cleaning script to convert country codes to ISO3, remove regional aggregates, label each three-year window with its middle year, and flag values reported as “<2.5”.

For Milestone 3, I organized the task split and timeline and narrowed the project scope after reviewing the course materials. I also updated the dataset descriptions in ProjectPlan.md to reflect our new sources, wrote the “Changes to the Project Plan” section, and put together this status report.

### 5.2 Hamza Ahmed

> **TODO – Hamza:** 2–4 sentences on your contributions. Commit from your own account.

### 5.3 Olusegun Fajinmi

> **TODO – Olusegun:** 2–4 sentences on your contributions. Commit from your own account.

### 5.4 Shannon Ahn

> **TODO – Shannon:** 2–4 sentences on your contributions. Commit from your own account.
