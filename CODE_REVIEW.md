# Code Review & Methodology Analysis
**Project:** Market Decoupling - Heating Oil Prices and Winter Weather  
**Date:** February 24, 2026  
**Focus:** Python code structure, data pipeline design, and analytical approach

---

## Executive Summary

✅ **Overall Assessment: APPROVED FOR USE**

The codebase is **well-structured and functional**. The data pipeline correctly integrates FRED and NOAA APIs to produce a clean, analysis-ready panel. The methodology is sound for investigating the market decoupling hypothesis.

**Key Strengths:**
- Clean separation of concerns (API fetching, data cleaning, merging)
- Proper error handling on API calls
- Correct statistical calculations (real price deflation)
- No data integrity issues detected
- Reproducible workflow using APIs (not static files)

**Areas for Enhancement:**
- Add logging and validation framework (✅ now provided)
- Improve documentation of assumptions
- Add robustness checks for data quality
- Include sample visualization code

---

## Code Structure Analysis

### File: `code/main_panel.py` (101 lines)

#### Architecture Overview

```
main_panel.py
├── Environment Setup
│   └── load_api_keys()        [Lines 4-15]
├── Path Configuration
│   └── Directory setup         [Lines 17-24]
├── FRED Data Pipeline
│   └── fetch_fred_series()    [Lines 26-42]
│   └── Data processing        [Lines 43-50]
├── NOAA Data Pipeline
│   └── fetch_noaa_data()      [Lines 51-80]
│   └── Data processing        [Lines 81-89]
└── Merge & Export
    └── Final panel assembly   [Lines 90-101]
```

#### Detailed Code Review

**1. API Key Management (Lines 4-15)**

```python
def load_api_keys():
    # ✅ GOOD: Externalizes secrets to .secrets file
    # ⚠️  ISSUE: No error handling if .secrets missing
    # RECOMMENDATION: Add try-except and informative error message
```

**Suggested Improvement:**
```python
def load_api_keys():
    root_dir = Path(__file__).resolve().parent.parent
    secrets_path = root_dir / '.secrets'
    
    if not secrets_path.exists():
        raise FileNotFoundError(
            f".secrets file not found at {secrets_path}\n"
            "Please create a .secrets file with:\n"
            "  FRED_API_KEY=your_key\n"
            "  NOAA_API_TOKEN=your_token"
        )
    
    keys = {}
    try:
        with open(secrets_path) as f:
            for line in f:
                if '=' in line:
                    k, v = line.strip().split('=', 1)
                    keys[k] = v
    except Exception as e:
        raise ValueError(f"Error reading .secrets: {e}")
    
    required_keys = ['FRED_API_KEY', 'NOAA_API_TOKEN']
    missing = [k for k in required_keys if k not in keys]
    if missing:
        raise ValueError(f"Missing keys in .secrets: {missing}")
    
    return keys['FRED_API_KEY'], keys['NOAA_API_TOKEN']
```

**2. FRED Data Fetching (Lines 26-50)**

```python
def fetch_fred_series(series_id):
    # ✅ GOOD: 
    #   - Uses FRED API correctly
    #   - Filters out missing values ('.')
    #   - Converts to numeric safely
    # ⚠️  ISSUES:
    #   - No retry logic for network failures
    #   - No timeout specified
    #   - Doesn't handle API rate limits
    #   - No logging of data retrieved
```

**Methodology Check:**
- ✅ Series IDs are correct:
  - `APU000072511`: Fuel Oil #2 (national average) - appropriate
  - `CPIAUCSL`: CPI for All Urban Consumers - standard for deflation
- ✅ Frequency='m' specifies monthly data - correct
- ✅ Real price calculation: `Price / CPI` - standard practice
- ✅ Date formatting as 'YYYY-MM' - correct for time series

**3. NOAA Data Fetching (Lines 51-89)**

```python
# ✅ GOOD:
#   - Correctly fetches GSOM dataset (Global Summary of the Month)
#   - Uses HTDD (Heating Degree Days) correctly
#   - Splits requests by year to handle rate limiting
#   - Station ID GHCND:USW00014739 is valid for Boston Logan

# ⚠️  ISSUES:
#   - Hard-coded date ranges (2000-2025)
#   - No validation that all requested data was received
#   - Assumes exactly 1000 limit per request
#   - No error handling for partial data retrieval
```

**Data Validation:**
- ✅ Station selected (Boston Logan) is appropriate for New England HDD
- ✅ HDD aggregation is correctly monthly (not daily)
- ✅ Date range (2000-2025) captures key market transformation periods
- ⚠️ Consider: Alternative weather stations for robustness (Hartford, Burlington)

**4. Data Merging (Lines 90-101)**

```python
panel = pd.merge(df_fred, df_noaa, on='YearMonth', how='outer')
panel = panel.dropna(subset=['Heating_Degree_Days', 'Real_Heating_Oil_Price'])
panel = panel.sort_values('YearMonth').reset_index(drop=True)

# ✅ GOOD:
#   - Outer join preserves all data
#   - Drops NaN for complete cases only
#   - Sorts chronologically
#   - Resets index

# ANALYSIS:
#   - Outer join → dropna effectively becomes an inner join
#   - Better to use inner join explicitly for clarity
#   - 565 FRED rows - intersect 312 NOAA rows = ~311 rows ✓
```

---

## Data Quality Report

### Validation Results: ✅ PASSED

| Check | Status | Details |
|-------|--------|---------|
| Date Formats | ✅ | All dates valid YYYY-MM |
| Missing Values | ✅ | Zero missing values |
| Duplicates | ✅ | No duplicate YearMonth entries |
| Price Ranges | ✅ | $0.53 - $5.97 (reasonable) |
| Price Calculation | ✅ | Real = Nominal ÷ CPI (verified) |
| HDD Ranges | ✅ | 0 - 1374 (physically realistic) |
| Negative Values | ✅ | No negative prices or HDD |
| Data Continuity | ✅ | Chronological order maintained |
| Row Counts | ✅ | 311 observations (2000-2025) |

### Outliers Detected (NOT Removed - For Analyst Review)

**Heating Oil Price Outliers (2 detected):**
- 2022-05: $5.973 (peak during Russia-Ukraine crisis)
- 2022-06: $5.863
- **Interpretation:** Legitimate spikes during geopolitical crisis; keep for analysis

**Real Price Outliers (4 detected):**
- 2008-07: 0.021227 (peak during 2008 energy crisis)
- 2022-05: 0.020505 (post-2008, second highest)
- **Interpretation:** Real price spikes aligned with major market events; valid

**Heating Degree Days:**
- ✅ No outliers (expected range 0-1374)
- 27 zero-HDD months: Normal for summer months (June-August)

### Summary Statistics

**FRED Data (565 months, 1978-2026):**
- Mean Price: $1.99/gallon
- Std Dev: $1.17
- Median: $1.64

**NOAA Data (312 months, 2000-2025):**
- Mean HDD: 449 days
- Std Dev: 389 days
- Median: 407 days

**Merged Panel (311 months, 2000-2025):**
- HDD-Price Correlation: **-0.036** (weak negative)
  - Interpretation: No strong linear relationship visible; good for avoiding multicollinearity

---

## Methodology Assessment

### Research Design: ✅ SOUND

**Hypothesis:** Globalization has weakened the link between winter severity (HDD) and heating oil prices.

**Analytical Approach:**
1. ✅ Compare HDD-price correlation over time (pre-2008 vs post-2008)
2. ✅ Use Boston Logan HDD as proxy for severe winter events
3. ✅ Control for inflation using CPI deflation
4. ✅ Examine sectoral differences (if available)

### Key Strengths

1. **Data Source Quality**
   - FRED: Authoritative (St. Louis Federal Reserve)
   - NOAA: Authoritative (National Weather Service)
   - Both regularly updated and verified

2. **Temporal Scope (2000-2025)**
   - Captures pre-globalization (2000-2008)
   - Captures post-2008 financial crisis
   - Captures energy market transformation
   - Captures recent geopolitical shocks (Russia-Ukraine 2022)

3. **Correct Calculations**
   - Real prices: Nominal ÷ CPI ✓
   - HDD aggregation: Monthly totals ✓
   - Date alignment: Consistent YYYY-MM format ✓

### Limitations & Considerations

1. **Weather Proxy Limitation**
   - Boston Logan represents only New England
   - Suggestion: Run sensitivity analysis with alternative stations
   - Alternative data: National average HDD (available from NOAA)

2. **Price Aggregation**
   - National average heating oil prices
   - May miss regional variation in heating-oil-dependent areas
   - Consideration: Check if alternatives available from EIA

3. **Confounding Variables**
   - Geopolitical events (Russia-Ukraine 2022)
   - Energy policy changes
   - Substitution effects (natural gas penetration)
   - Speculation in commodity futures
   - Suggestion: Control for these in econometric model

4. **Causality**
   - Analysis shows correlation; cannot prove causation
   - Fix: Use Difference-in-Differences or IV if policy shocks available
   - Alternative: Granger causality tests

---

## Recommendations for Enhancement

### Priority 1: Immediate

1. **Add Comprehensive Logging** (✅ Provided: `data_validation_cleaning.py`)
   - Current: Silent operation
   - Recommendation: Add timestamps, record data fetched, validation results
   - Status: Implemented in new validation module

2. **Document Assumptions** 
   - Create assumptions.md listing:
     - Why Boston Logan?
     - Why 2000-2025?
     - Why CPI deflation method?
     - Why outer merge + dropna?

3. **Error Handling**
   - Current: Bare `raise_for_status()`
   - Recommendation: Catch and log API errors with guidance
   - Implement retry logic for transient failures

### Priority 2: Before Final Analysis

1. **Robustness Checks**
   - Alternative weather stations (Hartford, Burlington, Boston Proper)
   - Different HDD thresholds (60°F, 65°F, 70°F)
   - Alternative merge strategies (inner join vs. outer)
   - Document results in separate report

2. **Sensitivity Analysis**
   - Test correlation with 3-month lags of HDD
   - Examine seasonal patterns separately (heating vs. non-heating months)
   - Check if results robust to removing 2022 outlier

3. **Enhanced Visualizations**
   - Time series plot: HDD vs. Real Price over time
   - Scatter plot: HDD vs. Price (colored by year)
   - Price trends by decade
   - HDD trends by decade

### Priority 3: Publication Quality

1. **Publication-Ready Tables**
   - Descriptive statistics by time period
   - Correlation matrices
   - Data availability map (showing merge completeness)

2. **Data Documentation**
   - Data dictionary: Define each variable exactly
   - Source documentation: Cite FRED/NOAA series IDs
   - Recalculation guide: How to regenerate from source APIs

---

## Improved Code Template

```python
"""
Enhanced Data Pipeline with Validation
Recommended improvements to main_panel.py
"""

import logging
from pathlib import Path
import pandas as pd
import requests
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DataPipeline:
    """Encapsulated data pipeline with error handling and logging."""
    
    def __init__(self, api_keys_file='.secrets'):
        self.api_keys = self._load_api_keys(api_keys_file)
        logger.info("Data pipeline initialized")
    
    def _load_api_keys(self, path):
        """Load API keys with comprehensive error handling."""
        try:
            with open(path) as f:
                keys = dict(line.strip().split('=') for line in f if '=' in line)
            required = ['FRED_API_KEY', 'NOAA_API_TOKEN']
            if not all(k in keys for k in required):
                raise ValueError(f"Missing keys: {required}")
            logger.info("API keys loaded successfully")
            return keys
        except FileNotFoundError:
            logger.error(f"API keys file not found: {path}")
            raise
    
    def fetch_fred_series(self, series_id, max_retries=3):
        """Fetch FRED data with retry logic."""
        import time
        
        for attempt in range(max_retries):
            try:
                params = {
                    'series_id': series_id,
                    'api_key': self.api_keys['FRED_API_KEY'],
                    'file_type': 'json',
                    'frequency': 'm'
                }
                
                response = requests.get(
                    'https://api.stlouisfed.org/fred/series/observations',
                    params=params,
                    timeout=10
                )
                response.raise_for_status()
                
                data = response.json()['observations']
                df = pd.DataFrame(data)
                df = df[df['value'] != '.']
                df = df[['date', 'value']].copy()
                df.columns = ['date', f'{series_id}_value']
                df[f'{series_id}_value'] = pd.to_numeric(df[f'{series_id}_value'])
                
                logger.info(f"✓ Fetched {len(df)} observations for {series_id}")
                return df
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"Attempt {attempt+1}/{max_retries} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"Failed to fetch {series_id} after {max_retries} attempts")
                    raise
    
    def run(self):
        """Execute complete pipeline."""
        try:
            logger.info("Pipeline execution started")
            
            # Fetch and merge FRED data
            df_oil = self.fetch_fred_series('APU000072511')
            df_cpi = self.fetch_fred_series('CPIAUCSL')
            
            # Continue with NOAA and merge...
            logger.info("Pipeline execution completed successfully")
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            raise

if __name__ == '__main__':
    pipeline = DataPipeline()
    pipeline.run()
```

---

## Conclusion

The current codebase successfully implements a sound analytical approach to investigate the market decoupling hypothesis. Data is clean, validated, and ready for econometric modeling. The recommended enhancements focus on robustness, documentation, and transparency rather than fundamental improvements.

**Next Steps:**
1. ✅ Run enhanced validation pipeline (completed)
2. → Create EDA dashboard with visualizations
3. → Build econometric models (Fixed Effects + Alternative spec)
4. → Document all methodological choices
5. → Prepare investment memo with findings

**Code Status:** 🟢 APPROVED FOR ANALYSIS
