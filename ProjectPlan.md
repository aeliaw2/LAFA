# Project Plan

**Economic Development, Food Insecurity, and Maternal Mortality Across Countries**

## 1. Overview
The goal of our project is to explore how economic development and food insecurity relate to maternal mortality across countries. We will look at how GDP per capita and the prevalence of undernourishment relate to maternal mortality. A major focus of this project is preparing the data so we can make reliable comparisons. We will start by checking each dataset for accuracy, completeness, timeliness, and consistency. Then, we will clean and integrate the data using standardized country codes and time periods. Once the datasets are combined, we will check the data again to make sure the integration did not introduce errors or inconsistencies. We will then use exploratory analysis and visualizations to look for patterns and relationships.

## 2. Team

### Team Members and Responsibilities

Abigail Liaw: Write the project overview, outline team responsibilities, develop the research questions, and describe the three datasets and their roles in the project. 
Hamza Ahmed: Identify potential constraints and challenges, document known gaps in the data or project plan, and highlight any additional information the team needs. 
Olusegun Fajinmi: Review ethical and legal considerations, develop the workflow and reproducibility plan, and create the project timeline. 
Shannon Ahn: Develop the data integration strategy, assess data quality, outline the cleaning process, and plan how the data and project files will be stored and organized.
All team members will contribute to the GitHub repository so that individual
contributions are documented through the commit history.

## 3. Research Questions

### Main Research Question

**How are economic development and food insecurity associated with maternal
mortality across countries?**

### Supporting Questions
1. Do countries with higher GDP per capita generally have lower maternal mortality rates?
2. Do countries with more undernourishment tend to have higher maternal mortality rates?
3. How have GDP per capita, undernourishment, and maternal mortality changed over time in different countries?

## 4. Datasets

### Dataset 1: World Development Indicators (World Bank)
**Source:** World Bank  
**File:** "WDICSV.csv"
**Description:** The World Development Indicators dataset includes economic, population, and health statistics for countries around the world. Its historical data will allow us to compare countries and track changes over time.
**Variables of Interest:** GDP per capita (current US$), Total population, Life expectancy at birth (years), Country name and country code, Year
**Role in Project:** This dataset will provide information about economic development and general health conditions. GDP per capita will be used to examine whether countries with higher levels of economic development have lower maternal mortality rates.
**Planned Integration Fields:** Country name/country code, Year

### Dataset 2: Suite of Food Security Indicators (FAOSTAT)
**Source:** Food and Agriculture Organization of the United Nations (FAO)  
**File:** "FAOSTAT_data_en_10-4-2026(1).csv"
**Description:** The FAOSTAT Suite of Food Security Indicators provides data on food security and nutrition across countries. Our selected dataset focuses on the prevalence of undernourishment, which measures the proportion of the population lacking sufficient dietary energy.
**Primary Indicator:** Prevalence of undernourishment (%) (three-year average)
**Additional Fields:** Area (country name), Area Code (M49), Year (three-year reporting period), Unit, Value
**Role in Project:** This dataset will measure food insecurity across countries. We will use the prevalence of undernourishment to investigate whether countries experiencing greater food insecurity also have higher maternal mortality rates.
**Planned Integration Fields:** Country/area name or standardized country code and Year, after aligning three-year reporting periods with annual observations

### Dataset 3: Maternal Mortality Ratio (United Nations)
**Source:** United Nations / Global SDG Database  
**File:** "SH_STA_MORT.csv"
**Description:** This dataset provides country-level estimates of maternal mortality over time. It focuses on deaths related to pregnancy and childbirth, giving us a way to compare maternal health outcomes across countries.
**Primary Indicator:** Maternal mortality ratio (maternal deaths per 100,000 live births)
**Additional Fields:** Geographic area identifier, Time period (year), Sex, Observation value
**Role in Project:** Maternal mortality will be the main health outcome in our analysis. By combining this dataset with the World Bank and FAOSTAT data, we will explore how maternal mortality ratios relate to economic development and food insecurity.
**Planned Integration Fields:** Geographic area identifier, mapped to a standardized country code, Year

## 5. Data Integration Strategy
We will build one country-year table linking GDP per capita (WDI), prevalence of undernourishment (FAOSTAT), and maternal mortality ratio (UN SDG).

Country key: each file labels countries differently, so we will convert them all to one standard 3-letter ISO3 code.
Time key: FAOSTAT gives 3-year averages, while others give single years. So we will pick the middle year and average the other datasets to match.

## 6. Data Quality Assessment

**Accuracy:** Check that units are correct and values are realistic (no negatives, no percentages over 100).

**Completeness:** Count missing values, countries, and years in each dataset.

**Timeliness:** Find the latest year in each dataset and the years all three share.

**Consistency:** Check that country names, codes, units, and year formats match across datasets.


## 7. Data Cleaning Plan
We will use Python scripts to select needed columns, reshape the World Bank data, standardize country codes and column names, remove regional groups, keep missing values as blank rather than filling them with assumptions, and align time periods across datasets.


## 8. Storage and Organization Strategy
We will use GitHub with separate folders for the original files, one for cleaned files, one for the final combined table, and one for code and notes.

## 9. Ethical and Legal Considerations

**Licenses used:**
- **FAOSTAT:** Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0), which allows sharing and adapting the data, including redistribution in our repository, as long as we give attribution.
- **UN Global SDG Database:** Governed by the UNdata terms of use. We will follow its attribution and citation requirements and note that we modified the data through cleaning and integration.
- **World Bank WDI:** Licensed under Creative Commons Attribution 4.0 International

**FAIR Principles:**
We will follow FAIR by:
- **Findable:** using a descriptive README, meaningful file names, and a metadata file (e.g., Schema.org).
- **Accessible:** hosting the project on GitHub.
- **Interoperable:** using open formats (CSV) and standard country codes.
- **Reusable:** including licenses for our code and data, a data dictionary, and documented provenance.

## 10. Workflow and Reproducibility Plan

Our workflow will be built from separate scripts that each do one job, tied together by a single run-all script that executes them in order, from data acquisition through data analysis. The scripts will:
- Download the three datasets and check their integrity with SHA-256 checksums
- Assess quality before integration (accuracy, completeness, timeliness, and consistency)
- Clean the country identifiers, years, and missing values
- Integrate the datasets in Python with pandas (including aligning FAOSTAT's three-year averages with annual data)
- Repeat the four-dimension quality assessment on the integrated data
- Run the analysis and create our visualizations

To make the project reproducible, it will:
- Run from beginning to end without code edits or path corrections, using relative paths
- Include a requirements file that declares our software, package versions, and data sources
- Include README instructions that state the exact order of steps from raw data to final results
- Upload input data to GitHub; any file over 50 MB will be hosted on Box with a download step in the workflow, a shareable link the TAs can access, and instructions for where to save the file in the project folder
- Include a data dictionary, a machine-readable metadata file (Schema.org, DCAT, or DataCite), and licenses for both our data and our code
- Ensure every team member commits their own work to GitHub so individual contributions show in the commit history

## 11. Timeline

Our project runs from the plan deadline on October 12 to the final release on December 7, with the interim status report due November 19, and we will use the Gantt chart below to track every task and overlap.

**Data Curation (First Priority):**
- Setup and acquisition (Oct 12-21)
- Pre-integration quality assessment (Oct 19-Nov 1)
- Cleaning (Oct 26-Nov 8)
- Integration (Nov 2-12)
- Post-integration quality checks (Nov 9-17)

**Reporting and Analysis (Follow-up):**
- Interim report (Nov 10-19)
- Analysis and visualization (Nov 18-28)
- Workflow, metadata, and documentation (Nov 20-Dec 3)
- Final README and GitHub release (Dec 1-7)

We will review the Gantt chart and adjust dates if a stage runs long or shorter than expected.
