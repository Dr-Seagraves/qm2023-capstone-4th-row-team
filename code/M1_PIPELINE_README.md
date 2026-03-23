# Milestone 1: Data Pipeline - Technical Documentation

**Capstone Project:** Market Decoupling Analysis  
**Milestone:** 1 (Data Pipeline)  
**Status:** Submission Ready  
**Due:** Week 5 (February 20, 2026)

---

## 📋 Overview

This Milestone 1 deliverable documents the end-to-end data pipeline that fetches, validates, cleans, and merges heating oil price and weather data into an analysis-ready panel dataset.

### Pipeline Objective
Construct a clean, tidy monthly time-series panel (2000-2025) combining:
- **Economic Data:** Heating oil prices and CPI inflation measures (FRED API)
- **Climate Data:** Heating degree days at Boston Logan (NOAA API)
- **Analytical Purpose:** Test hypothesis of market decoupling (price insulation from weather)

### Deliverables
1. ✅ Python data pipeline script (`code/main_panel.py`)
2. ✅ Enhanced validation module (`code/data_validation_cleaning.py`)
3. ✅ Final merged dataset (`data/final/final.csv` - 311 rows × 5 cols)
4. ✅ Enhanced dataset with calculated features (`data/final/final_enhanced.csv` - 311 rows × 15 cols)
5. ✅ Comprehensive validation report (`DATA_CLEANING_REPORT.md`)
6. ✅ Data dictionary (`DATA_DICTIONARY.md`)

---

## 🏗️ Pipeline Architecture

### Stage 1: Data Acquisition (API Fetching)

#### FRED API - Economic Data
```
┌─────────────────────────────────┐
│    FRED API (STL Federal Res)   │
└────────────┬────────────────────┘
             │
      ┌──────┴──────┐
      │             │
   Series 1      Series 2
      │             │
    APU0005      CPIAUCSL
   072511          (CPI)
      │             │
Heating Oil    Inflation
  Prices       Adjustment
      │             │
      └──────┬──────┘
             │
      Merge on DATE
             │
    ┌────────▼────────┐
    │  FRED DataFrame  │
    │  565 rows × 3    │
    │  cols (1978-26)  │
    └──────────────────┘
```

**Series Details:**
- **APU000072511:** Average Price: Fuel Oil #2 (Residential)
  - Frequency: Monthly
  - Units: $/gallon (nominal)
  - Range: $0.533 - $5.973
  - Source: U.S. Bureau of Labor Statistics

- **CPIAUCSL:** Consumer Price Index for All Urban Consumers
  - Frequency: Monthly  
  - Index Base: 1982-84 = 100
  - Range: 67.5 - 326.6
  - Use: Deflator for real price calculation

**Data Processing:**
- Filter out missing values (marked as '.')
- Convert to numeric type
- Handle NaN appropriately
- Date format: YYYY-MM

#### NOAA API - Climate Data
```
┌──────────────────────────────┐
│   NOAA CDO Web Services      │
└────────────┬───────────────────┘
             │
      Dataset: GSOM
      Element: HTDD
      │
      └─→ Boston Logan Airport
          ID: GHCND:USW00014739
          │
          │ Request by year range:
          ├─→ 2000-01 to 2009-12
          ├─→ 2010-01 to 2019-12
          └─→ 2020-01 to 2025-12
             │
             ├─→ Concatenate results
             │
             └─→ Year-month aggregation
                │
      ┌─────────▼──────────┐
      │ NOAA DataFrame     │
      │ 312 rows × 2 cols  │
      │ (2000-2025)        │
      └────────────────────┘
```

**Dataset Details:**
- **GSOM:** Global Summary of the Month
- **HTDD:** Heating Degree Days
- **Station:** Boston Logan Airport (WBAN code 14739)
  - Geographic: New England (high heating oil consumption)
  - Rationale: Representative for winter severity proxy
  - Data Quality: Consistent long-term records

**Data Processing:**
- Request in 10-year chunks (rate limiting)
- Extract date and HDD value
- Convert to numeric
- Aggregate daily → monthly (sum all daily HDD for month)
- Date format: YYYY-MM

### Stage 2: Data Cleaning

#### FRED Data Cleaning
```
Raw FRED Data
      │
      ├─→ Filter out '.' (missing) values
      │
      ├─→ Merge APU000072511 + CPIAUCSL on date
      │
      ├─→ Calculate real price: Nominal ÷ CPI
      │
      ├─→ Rename columns:
      │   - value_Nominal → Heating_Oil_Price
      │   - value_CPI → CPI
      │
      ├─→ Format date as YearMonth (YYYY-MM)
      │
      ├─→ Select final columns
      │
      └─→ Validated FRED DataFrame
          (565 rows × 4 cols)
```

**Cleaning Logic:**
- Remove missing values marked as '.' (FRED convention)
- Numeric type conversion with error handling
- Real price = Nominal ÷ CPI (accounts for inflation)
- Consistent date formatting

#### NOAA Data Cleaning
```
Raw NOAA Data
      │
      ├─→ Extract relevant columns
      │
      ├─→ Convert dates to YearMonth format
      │
      ├─→ Rename: value → Heating_Degree_Days
      │
      ├─→ Ensure numeric type
      │
      ├─→ No filtering (keep all HDD values including 0)
      │
      └─→ Validated NOAA DataFrame
          (312 rows × 2 cols)
```

**Cleaning Logic:**
- Extract date and value columns
- Aggregation already done (monthly total HDD)
- Keep zero-HDD months (summer months are valid)
- No imputation applied

### Stage 3: Data Merge & Final Preparation

#### Merge Strategy
```
FRED DataFrame          NOAA DataFrame
(565 rows)              (312 rows)
     │                       │
     │   Merge on:           │
     │   YearMonth           │
     │                       │
     └──────────┬────────────┘
                │
         Outer Join
         (preserves all data)
                │
       ┌────────▼────────┐
       │ Merged DataFrame │
       │ 565 outer + 312  │
       │ overlaps         │
       └────────┬────────┘
                │
       ├─→ Drop rows with NaN
       │   in required columns:
       │   - Heating_Degree_Days
       │   - Real_Heating_Oil_Price
       │
       └─→ Complete Cases
           (311 rows)
           2000-01 to 2025-12
```

**Merge Justification:**
- **Outer join:** Preserves all available data initially
- **dropna:** Requires both variables present for analysis
- **Complete case analysis:** Valid when data Missing Completely At Random (MCAR)
- **Result:** 311 monthly observations with no missing values

#### Final DataFrame Structure

| Column | Type | Observations |
|--------|------|--------------|
| YearMonth | String | Time identifier |
| Heating_Oil_Price | Float | Nominal price |
| CPI | Float | Inflation index |
| Real_Heating_Oil_Price | Float | Adjusted price (primary) |
| Heating_Degree_Days | Float | Weather severity |

**Data Quality Checks:**
- ✅ Zero missing values
- ✅ Chronological order maintained
- ✅ Date format consistency
- ✅ No duplicate entries
- ✅ Real price calculation verified

---

## 💾 File Output Specifications

### Primary Output: final.csv
- **Location:** `data/final/final.csv`
- **Format:** CSV (comma-delimited)
- **Encoding:** UTF-8
- **Rows:** 311 observations
- **Columns:** 5 variables
- **Size:** ~15 KB
- **Content:** Analysis-ready merged panel

### Enhanced Output: final_enhanced.csv
- **Location:** `data/final/final_enhanced.csv`
- **Format:** CSV (comma-delimited)
- **Encoding:** UTF-8
- **Rows:** 311 observations
- **Columns:** 15 variables (5 original + 10 calculated)
- **Size:** ~45 KB
- **Content:** Features for advanced analysis
- **Additional Features:**
  - Date/time components (Year, Month, Quarter)
  - Price dynamics (Change, % Change, Moving Average)
  - Weather categories and lags

### Intermediate Files (for reproducibility)
- **fred_clean.csv:** Cleaned FRED data (565 rows × 4 cols)
- **noaa_clean.csv:** Cleaned NOAA data (312 rows × 2 cols)

---

## 🚀 How to Execute the Pipeline

### Prerequisites
```bash
# Required Python packages
pip install pandas requests

# API credentials required
# Create file: .secrets
# Contents:
#   FRED_API_KEY=your_key_here
#   NOAA_API_TOKEN=your_token_here

# Get keys from:
# FRED: https://fred.stlouisfed.org/docs/api/api_key.html
# NOAA: https://www.ncei.noaa.gov/cdo-web/token
```

### Step 1: Set Up Environment
```bash
# Create .secrets file with API credentials
cat > .secrets << EOF
FRED_API_KEY=YOUR_KEY_HERE
NOAA_API_TOKEN=YOUR_TOKEN_HERE
EOF

# Verify file created
ls -la .secrets
```

### Step 2: Run Pipeline
```bash
# Execute main data pipeline
python code/main_panel.py

# Expected output:
# "Saved cleaned FRED data: 565 rows."
# "Saved cleaned NOAA data: 312 rows."
# "Final panel shape: (311, 5)"
# "Saved merged panel to data/final/final.csv"
```

### Step 3: Validate Results
```bash
# Run comprehensive validation
python code/data_validation_cleaning.py

# Expected output:
# - Data quality report with all checks ✅ PASSED
# - Enhanced dataset created with 15 columns
# - Validation log written to results/logs/data_validation.log
```

### Step 4: Verify Output
```bash
# Check final dataset
head -5 data/final/final.csv

# Expected first row:
# YearMonth,Heating_Oil_Price,CPI,Real_Heating_Oil_Price,Heating_Degree_Days
# 2000-01,1.189,169.3,0.0070230360307147075,1163.0
```

---

## 📊 Data Quality Summary

### Validation Results: ✅ ALL PASSED

| Check | Result | Details |
|-------|--------|---------|
| Date Format | ✅ | 877 dates valid (YYYY-MM) |
| Missing Values | ✅ | 0 missing in final dataset |
| Duplicates | ✅ | 0 duplicate entries |
| Negative Values | ✅ | 0 negative prices or HDD |
| Price Calculation | ✅ | Real = Nominal ÷ CPI verified |
| Data Continuity | ✅ | Chronological order maintained |
| Row Counts | ✅ | 311 final observations (correct merge) |

### Outliers (Identified, Retained)
- **2022-05 & 2022-06:** Price peaks ($5.97, $5.86) - Russia-Ukraine crisis
- **2008-06 & 2008-07:** Real price peaks (0.021) - Energy/financial crisis
- **Decision:** RETAINED - legitimate market events not errors

---

## 📝 Cleaning Decisions Documentation

### Missing Value Strategy
**Approach:** Complete case deletion (outer merge + dropna)

**Rows Processed:**
- FRED data: 565 observations (1978-2026)
- NOAA data: 312 observations (2000-2025)
- After merge: 565 rows (outer join)
- After filtering: 311 rows (complete cases)
- **Rows lost:** 254 (mostly pre-2000 FRED data without NOAA match)

**Justification:**
- Analysis requires both price AND weather data
- Temporal restriction to 2000-2025 is analytical choice
- MCAR assumption appropriate (no systematic reason for missing)

### Real Price Deflation Method
**Formula:** Real_Price = Nominal_Price ÷ CPI × 100

**Alternative considered:** Fixed base year (2000=100)
**Decision:** Point-in-time relative value chosen for interpretability

### Date Alignment
**Format:** YYYY-MM (consistent with analysis frequency)
**Timezone:** Not applicable (monthly aggregates, no intraday data)
**Leap year handling:** Not applicable (monthly frequency)

### HDD Aggregation
**Method:** Monthly sum of daily HDD values
**Formula:** HDD = sum of max(0, 65°F - daily_mean_temp) for each day
**Rationale:** Standard approach in heating economics; captures cumulative cold exposure

---

## ✅ Checklist for M1 Submission

- [x] Python pipeline script (`main_panel.py`) - functional
- [x] Data fetching from APIs working
- [x] Data cleaning with documented decisions
- [x] Data merge on common date field
- [x] Tidy panel format (Entity=location, Time=month)
- [x] Final CSV output (final.csv)
- [x] Row count verification (311 complete observations)
- [x] Relative paths (no hardcoded C:\Users\)
- [x] Data validation report
- [x] Data dictionary
- [x] Pipeline documentation (this file)
- [x] Enhanced dataset with analytical features
- [x] Validation logging

---

## 🔗 Related Documentation

- **Data Dictionary:** `data/final/DATA_DICTIONARY.md` - Variable definitions
- **Quality Report:** `DATA_CLEANING_REPORT.md` - Validation results
- **Code Review:** `CODE_REVIEW.md` - Python code analysis
- **AI Audit:** `AI_AUDIT.md` - AI usage transparency
- **Project Status:** `PROJECT_STATUS.md` - Overall progress

---

## 📞 Support & Reproducibility

### Troubleshooting
- **API timeout:** Increase timeout in requests.get()
- **Rate limiting:** Pipeline uses year-ranges to minimize API stress
- **Missing .secrets:** Create file with FRED_API_KEY and NOAA_API_TOKEN

### Reproducibility Notes
- Pipeline is fully API-based (no static files)
- Reproducible on any machine with internet & correct credentials
- Python 3.7+ compatible
- Pandas 1.0+ required

### Future Enhancements
- Error handling with retry logic
- Logging framework for debugging
- Unit tests for data validation
- Alternative weather station comparisons
- Regional price data (if available)

---

**Status:** ✅ READY FOR M1 SUBMISSION  
**Last Updated:** 2026-02-24  
**Due Date:** 2026-02-20 (Submitted Late)
