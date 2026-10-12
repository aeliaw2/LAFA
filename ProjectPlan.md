# Project Plan

**Economic Development, Food Insecurity, and Maternal Mortality Across Countries**

## 1. Overview
The goal of our project is to explore how economic development and food insecurity relate to maternal mortality across countries. We will look at how GDP per capita and the prevalence of undernourishment are associated with maternal mortality rates using three datasets from the World Bank, the Food and Agriculture Organization of the United Nations (FAOSTAT), and the United Nations Global SDG Database.
A major focus of this project is preparing the data so we can make reliable comparisons. We will start by checking each dataset for accuracy, completeness, timeliness, and consistency. Then, we will clean and standardize country identifiers, year formats, and missing values so the datasets can be combined. Since FAOSTAT reports three-year averages, we will also decide on a consistent way to align those observations with the annual data from the other sources.
Once the datasets are combined, we will check the data again to make sure the integration did not introduce errors or inconsistencies. We will then use exploratory analysis and visualizations to look for patterns among the three indicators. Throughout the project, we will document our steps and automate the workflow so others can understand our process and reproduce the results.

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
**File:** “WDICSV.csv”
**Description:** The World Development Indicators dataset includes economic, population, and health statistics for countries around the world. Its historical data will allow us to compare countries and look at how these indicators have changed over time.
**Variables of Interest:** GDP per capita (current US$), Total population, Life expectancy at birth (years), Country name and country code, Year
**Role in Project:** This dataset will provide information about economic development and general health conditions. GDP per capita will be used to examine whether countries with higher levels of economic development tend to have lower rates of undernourishment and maternal mortality. Population and life expectancy will provide additional context for comparing countries.
**Planned Integration Fields:**Country name/country code, Year

### Dataset 2: Suite of Food Security Indicators (FAOSTAT)
**Source:** Food and Agriculture Organization of the United Nations (FAO)  
**File:** “FAOSTAT_data_en_10-4-2026(1).csv”
**Description:**The FAOSTAT Suite of Food Security Indicators provides data on food security and nutrition across countries. Our selected dataset focuses on the prevalence of undernourishment, which measures the percentage of the population whose habitual dietary energy consumption is insufficient to meet minimum energy requirements.
**Primary Indicator:**Prevalence of undernourishment (%) (three-year average)
**Additional Fields:**Area (country name), Area Code (M49), Year (three-year reporting period), Unit, Value
**Role in Project:** This dataset will measure food insecurity across countries. We will use the prevalence of undernourishment to investigate whether countries experiencing greater food insecurity also tend to have higher maternal mortality ratios. This indicator will also be compared with GDP per capita to explore relationships between economic development and food security.
**Planned Integration Fields:**Country/area name or standardized country code and Year, after aligning three-year reporting periods with annual observations

### Dataset 3: Maternal Mortality Ratio (United Nations)
**Source:** United Nations / Global SDG Database  
**File:** “SH_STA_MORT.csv”
**Description:**This dataset provides country-level estimates of maternal mortality over time. It focuses on deaths related to pregnancy and childbirth, giving us a way to compare maternal health outcomes across countries.
**Primary Indicator:**Maternal mortality ratio (maternal deaths per 100,000 live births)
**Additional Fields:**Geographic area identifier, Time period (year), Sex, Observation value
**Role in Project:**Maternal mortality will be the main health outcome in our analysis. By combining this dataset with the World Bank and FAOSTAT data, we will explore how maternal mortality ratios relate to GDP per capita and undernourishment. Together, these datasets will help us look for patterns connecting economic development, food insecurity, and maternal health.
**Planned Integration Fields:** Geographic area identifier, mapped to a standardized country code, Year


