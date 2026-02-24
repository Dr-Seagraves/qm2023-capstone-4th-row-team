# QM 2023 Capstone: The Market Decoupling

This repository contains the data pipeline for our macro-finance research question:

**"The Market Decoupling: Has the globalized energy supply chain severed the link between severe US winters and domestic heating oil prices?"**

## Project Overview

This project builds a clean data panel to analyze the relationship between US winter severity and real heating oil prices. It automatically fetches, processes, and merges data from two key sources to create a final, analysis-ready dataset.


### Data Sources & Regional Focus

<<<<<<< HEAD
*   **Economic Data:** Federal Reserve Economic Data (FRED) API
    *   `APU000072511`: Average Price: Fuel Oil #2 (monthly, national average)
    *   `CPIAUCSL`: Consumer Price Index for All Urban Consumers (used to calculate real prices)



*   **Climate Data:** NOAA Climate Data Online (CDO) Web Services API
    *   `GSOM` (Global Summary of the Month) dataset
    *   `HTDD` (Heating Degree Days) for Boston Logan station (WBAN:14739)

#### Why Boston Logan?
Boston Logan is a major weather station in New England, a region with high heating oil usage and severe winters. NOAA provides more complete data for this station, allowing for a richer panel.

#### How HDD Is Aggregated
Heating Degree Days (HDD) are summed for each month at Boston Logan, producing a single monthly value. This is standard for HDD analysis and allows direct comparison to monthly heating oil prices.

## How to Run the Pipeline

To generate the final dataset, follow these steps:

### 1. Set Up Your Environment

Create a `.env` file in the root of this project. This file will store your API keys and should not be committed to Git.

Your `.env` file should look like this:

```
FRED_API_KEY="YOUR_FRED_API_KEY_HERE"
NOAA_TOKEN="YOUR_NOAA_API_TOKEN_HERE"
```

*You can obtain a FRED API key [here](https://fred.stlouisfed.org/docs/api/api_key.html).*
*You can obtain a NOAA API token [here](https://www.ncdc.noaa.gov/cdo-web/token).*

### 2. Run the Build Script


Execute the main data pipeline script from your terminal:

```bash
python code/build_analysis_panel.py
```

### 3. Verify the Output



The script will perform the following actions:
1. Ensure the necessary `data/raw`, `data/processed`, and `data/final` directories exist.
2. Fetch the latest data from the FRED and NOAA APIs.
3. Clean the data:
    - FRED: Heating oil price and CPI are merged and real prices calculated (national average).


    - NOAA: Heating Degree Days (HDD) values are summed for each month at Boston Logan (WBAN:14739) to produce a single monthly value.
4. Merge the two datasets into a single time-series panel, aligning Boston Logan's HDD with national heating oil prices.
5. Save the final output to `data/final/market_decoupling_panel.csv`.

The script will print the final shape of the dataset upon completion.

## Data Cleaning & Merging Details

- **FRED Data:**
    - Downloaded via API for each month from 1978 onward.
    - Heating oil price and CPI are merged; real prices are calculated by dividing nominal price by CPI.


- **NOAA Data (Boston Logan):**
    - Downloaded via API for Boston Logan station (WBAN:14739) for each month.
    - All daily HDD values are summed to produce a single monthly HDD value for Boston Logan.
- **Merging:**
    - The two datasets are merged on YearMonth.
    - The final panel contains: YearMonth, Heating_Oil_Price, CPI, Real_Heating_Oil_Price, Heating_Degree_Days (Boston Logan).

This approach allows analysis of how severe cold snaps in Boston (a high heating oil usage region) relate to national heating oil prices, testing whether the price response to extreme weather has changed over time.


