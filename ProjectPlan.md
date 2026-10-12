# Economic Development, Food Insecurity, and Maternal Mortality Across Countries

**5. Data Integration Strategy**

We will build one country-year table linking GDP per capita (WDI), prevalence of undernourishment (FAOSTAT), and maternal mortality ratio (UN SDG).

**Country key:** each file labels countries differently, so we wikk convert them all to one standard 3-letter ISO3 code.
**Time key:** FAOSTAT gives 3 year averages, while others give single years. So we will pick the middle year and average the other datasets to match.

**6. Data Quality Assessment** 

**Accuracy:** Check that units are correct and values are realistic (no negatives, no percentages over 100).

**Completeness:** Count missing values, countries, and years in each dataset.Count missing values, countries, and years in each dataset.

**Timeliness:** Find the latest year in each dataset and the years all three share.

**Consistency:**  Check that country names, codes, units, and year formats match across datasets.

**7. Data Cleaning Plan** 
We will use Python scripts to select needed columns, reshape the World Bank data, standardize country codes and column names, remove regional groups, keep missing values as blank rather than filling them in, and log every change we make.

**8. Storage and Organization Strategy**
We will use GitHub with separate folders for the original files, one for cleaned files, one for the final combined table, and one for code and notes.
