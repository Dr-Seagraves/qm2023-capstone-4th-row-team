# Data Dictionary - Final Analysis Panel

**Project:** Market Decoupling - Heating Oil Prices and Winter Weather Analysis  
**Primary Dataset:** final_enriched.csv (10 columns — use this for all M2/M3 analysis)  
**Base Dataset:** final.csv (5 columns — raw pipeline output)  
**Observations:** 311 (January 2000 – December 2025; October 2025 missing from NOAA)  
**Data Type:** Monthly time series (single entity; no panel structure)

**Last Updated:** 2026-04-12 (geographic mismatch fix: replaced single-station Boston Logan HDD with EIA population-weighted regional HDD)

---

## Primary Analysis Variables (in final_enriched.csv)

| Variable Name | Data Type | Range | Units | Source | Description |
|---------------|-----------|-------|-------|--------|-------------|
| YearMonth | String | 2000-01 to 2025-12 | — | Merged | Time period identifier |
| Heating_Oil_Price | Float64 | 1.112 to 5.973 | $/gallon | FRED APU000072511 | Nominal average price of Fuel Oil #2, national |
| CPI | Float64 | 168.8 to 326.6 | Index (1982-84=100) | FRED CPIAUCSL | Deflator for real price calculation |
| Real_Heating_Oil_Price | Float64 | 0.005 to 0.021 | Nominal/CPI ratio | Calculated | Legacy ratio; multiply by CPI_2020 ≈ 258.86 for $/gal |
| **NEC_HDD** | Float64 | 0 to ~1800 | Degree-days | **EIA STEO ZWHD_NEC** | **PRIMARY DRIVER — New England Census Division (MA/ME/NH/VT/CT/RI) HDD, population-weighted. Matches geographic scope of heating oil consumption (~75% of U.S. use). Use this in all regressions.** |
| US_HDD | Float64 | 0 to ~1100 | Degree-days | EIA STEO ZWHDPUS | U.S. national average HDD, population-weighted — used as robustness check in M3 |
| MAC_HDD | Float64 | 0 to ~1400 | Degree-days | EIA STEO ZWHD_MAC | Middle Atlantic (NY/NJ/PA) HDD — additional robustness |
| Boston_HDD | Float64 | 0.0 to 1374.0 | Degree-days | NOAA GSOM, GHCND:USW00014739 | **Legacy single-station HDD (Boston Logan Airport). Retained for comparison only. Do NOT use as primary driver — single-station measurement error attenuates OLS estimates.** |
| WTI_Price | Float64 | 16.55 to 133.88 | $/barrel | FRED MCOILWTICO | WTI Crude Oil Price — dominant global price determinant (r = +0.946 with real heating oil price) |
| HenryHub_Price | Float64 | 1.49 to 13.42 | $/MMBtu | FRED MHHNGSP | Henry Hub Natural Gas Spot Price — substitute fuel price signal |

---

## Base Variables (in final.csv — raw pipeline output)

| Variable Name | Source | Notes |
|---------------|--------|-------|
| YearMonth | Merged | |
| Heating_Oil_Price | FRED APU000072511 | |
| CPI | FRED CPIAUCSL | |
| Real_Heating_Oil_Price | Calculated | Nominal/CPI ratio |
| Heating_Degree_Days | NOAA GSOM USW00014739 | Boston Logan single station; renamed to `Boston_HDD` in final_enriched.csv |

---

## Enhanced Variables (additional columns in final_enhanced.csv)

| Variable Name | Data Type | Format | Description | Calculation |
|---------------|-----------|--------|-------------|-------------|
| Date | Datetime | YYYY-MM-DD | Parsed datetime object (first day of month) | pd.to_datetime(YearMonth) |
| Year | Int64 | YYYY | Calendar year (2000-2025) | Extract from YearMonth |
| Month | Int64 | 1-12 | Calendar month (Jan=1, Dec=12) | Extract from YearMonth |
| Quarter | Int64 | 1-4 | Calendar quarter (Q1=Jan-Mar, etc.) | Month grouped to quarters |
| Price_Change | Float64 | $/gallon | Month-over-month change in real price | Real_Heating_Oil_Price.diff() |
| Price_PctChange | Float64 | Percent (0-1) | Month-over-month percentage change | Real_Heating_Oil_Price.pct_change() |
| Price_MA3 | Float64 | Price/CPI | 3-month moving average of real price | Real_Heating_Oil_Price.rolling(3).mean() |
| HDD_Category | Categorical | Warm/Mild/Cold/Severe | Categorical classification of heating severity | Binned: 0-50=Warm, 51-300=Mild, 301-800=Cold, 801+=Severe |
| HDD_Lag1 | Float64 | Degrees | Heating degree days from previous month | Heating_Degree_Days.shift(1) |
| HDD_Lag3 | Float64 | Degrees | Heating degree days from 3 months prior | Heating_Degree_Days.shift(3) |

---

## Data Quality Notes

### Missing Values
- **Final Dataset:** 0 missing values
- **Treatment:** Outer merge followed by complete-case deletion
- **Rationale:** Analysis requires both price AND weather data; 311 complete observations from 2000-2025

### Outliers Detected (Retained)
- **Heating Oil Price outliers (2 detected):**
  - 2022-05: $5.973 (peak) - Russia-Ukraine geopolitical crisis
  - 2022-06: $5.863 - continued crisis period
  - **Decision:** KEPT - legitimate market events

- **Real Price outliers (4 detected):**
  - 2008-07: 0.021227 (peak) - 2008 energy/financial crisis
  - 2008-06: 0.021102 - crisis period
  - 2022-05: 0.020505 - geopolitical shock
  - **Decision:** KEPT - represent important historical price movements

- **HDD outliers:**
  - None detected (0-1374 is physically realistic for New England)

### Zero HDD Values (27 months)
- **Months affected:** June, July, August (typical summer months)
- **Reason:** Heating degree days equal zero during warm months (no heating required)
- **Status:** EXPECTED AND VALID - kept for complete time series

---

## Temporal Coverage

| Component | Start | End | Months | Coverage |
|-----------|-------|-----|--------|----------|
| FRED Data | 1978-11 | 2026-01 | 565 | 47+ years |
| NOAA Data | 2000-01 | 2025-12 | 312 | 26 years |
| **Merged Panel** | **2000-01** | **2025-12** | **311** | **26 years** |

---

## Data Source Details

### FRED (Federal Reserve Economic Data)
- **Series 1:** APU000072511 - Average Price: Fuel Oil #2
  - Frequency: Monthly
  - Units: Dollars per gallon
  - Geographic Level: National average
  - Data Provider: U.S. Department of Labor
  
- **Series 2:** CPIAUCSL - Consumer Price Index for All Urban Consumers
  - Frequency: Monthly
  - Index Base: 1982-84 = 100
  - Coverage: All U.S. urban consumers
  - Use: Deflator for real price calculation

### NOAA (National Oceanic & Atmospheric Administration)
- **Dataset:** GSOM (Global Summary of the Month)
- **Element:** HTDD (Heating Degree Days)
- **Station:** Boston Logan Airport (ID: GHCND:USW00014739)
  - Latitude: 42.37°N, Longitude: 71.01°W
  - Elevation: 5 feet
  - Region: Massachusetts, New England
  - **Rationale:** High heating oil consumption region; reliable long-term weather data
  
- **Calculation:** Daily HDD summed to monthly total
- **HDD Formula:** Sum of (65°F - daily mean temperature) for days where mean < 65°F

---

## Analytical Recommendations

### When Using This Data
1. **Real Prices:** Always use `Real_Heating_Oil_Price` (not nominal) for time-series analysis
2. **Lagged Effects:** Use `HDD_Lag1` and `HDD_Lag3` to test delayed weather impacts
3. **Seasonality:** Control for `Month` or `Quarter` in models (strong heating seasonality)
4. **Subperiod Analysis:** Compare pre-2008 (financial crisis) vs. post-2015 (post-crisis recovery)
5. **Weather Categories:** Use `HDD_Category` for non-linear heating demand analysis

### Limitations
- **Monthly frequency:** Daily cold spikes (polar vortex events) are averaged away; weekly data would reveal sharper short-run effects
- **Selection Bias:** Analysis restricted to months with both price and HDD data (MCAR assumption)
- **Confounders:** Prices also reflect geopolitics, speculation, substitution effects (natural gas)
- **Causality:** Correlation analysis and dynamic OLS; cannot establish clean causal mechanisms without a natural experiment

---

## File Specifications

| Filename | Format | Encoding | Delimiter | NaN Symbol |
|----------|--------|----------|-----------|-----------|
| final.csv | CSV | UTF-8 | Comma (,) | None (values present) |
| final_enhanced.csv | CSV | UTF-8 | Comma (,) | NaN (Python float) |

---

## Recalculation Guide

To regenerate this dataset from source APIs:

```python
# Run this script to regenerate final.csv:
python code/main_panel.py

# Run this script for validation and enhancement:
python code/data_validation_cleaning.py

# Output locations:
# - Original: data/final/final.csv (311 rows × 5 cols)
# - Enhanced: data/final/final_enhanced.csv (311 rows × 15 cols)
```

---

**Data Dictionary Created:** 2026-02-24  
**Last Updated:** 2026-02-24  
**Verification Status:** ✅ All variables documented and validated
