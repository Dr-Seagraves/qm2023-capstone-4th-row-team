# QM 2023 Capstone: The Market Decoupling

**"Has the globalized energy supply chain severed the link between severe US winters and domestic heating oil prices?"**

## Research Question & Hypothesis

Historically, harsh US winters drove heating oil prices higher as local demand surged and supply chains struggled to respond. This project examines whether globalization of energy markets has weakened this relationship over time. As energy supply chains became more integrated internationally and alternative energy sources proliferated, we hypothesize that **the sensitivity of heating oil prices to extreme US winter weather has diminished**.

## Analytical Approach

### Core Relationship

We analyze the relationship between:
- **Winter Severity**: Measured by Heating Degree Days (HDD) at Boston Logan Airport
- **Real Heating Oil Prices**: National average Fuel Oil #2 prices, adjusted for inflation

The fundamental question is whether HDD fluctuations predict price movements, and critically, **whether this predictive power has changed over recent decades**.

### Why Boston Logan?

Boston Logan serves as our climate proxy for several analytical reasons:
1. **Regional Relevance**: New England has historically been the largest heating oil consumption region in the US
2. **Weather Extremes**: The station captures significant winter severity variation
3. **Data Quality**: NOAA provides complete, consistent monthly HDD measurements for this location

By pairing regional climate data with national prices, we can test whether local weather shocks still drive national market outcomes—or whether markets have decoupled from regional weather patterns.

### Temporal Dimension

The analysis spans 2000-2025, a period of significant energy market transformation:
- Expansion of global LNG trade
- Growth of alternative heating sources (natural gas, electricity)
- Increased pipeline capacity and storage infrastructure
- More sophisticated commodity futures markets

If globalization has insulated prices from local weather, we expect:
- **Weaker correlation** between HDD and prices in recent years
- **Reduced price volatility** during extreme weather events
- **Delayed or muted price responses** to cold snaps

### Variables in the Analysis Panel

The final dataset contains monthly observations with:
- `YearMonth`: Time identifier
- `Heating_Degree_Days`: Monthly HDD at Boston Logan (higher = colder)
- `Heating_Oil_Price`: Nominal price per gallon (USD)
- `CPI`: Consumer Price Index for inflation adjustment
- `Real_Heating_Oil_Price`: Inflation-adjusted price (primary outcome variable)

## Interpretation Framework

This analysis provides evidence for or against the "market decoupling" hypothesis:

**Evidence FOR decoupling** would include:
- Declining correlation between HDD and real prices over time
- Reduced price spikes during high-HDD months in recent years
- Statistical tests showing structural breaks in the relationship

**Evidence AGAINST decoupling** would include:
- Persistent strong correlation throughout the time series
- Similar price responses to weather shocks across decades
- No significant change in the HDD-price relationship

---

## Running the Analysis Pipeline

To replicate this analysis:

### 1. Configure API Access

Create a `.secrets` file in the project root:

```
FRED_API_KEY=your_fred_api_key
NOAA_API_TOKEN=your_noaa_token
```

*Obtain keys from [FRED](https://fred.stlouisfed.org/docs/api/api_key.html) and [NOAA CDO](https://www.ncdc.noaa.gov/cdo-web/token).*

### 2. Execute the Pipeline

```bash
python code/main_panel.py
```

This will:
- Fetch monthly heating oil prices and CPI from FRED (2000-present)
- Retrieve Heating Degree Days for Boston Logan from NOAA
- Calculate real (inflation-adjusted) prices
- Merge climate and economic data by month
- Output the analysis-ready panel to `data/final/final.csv`

### 3. Output

The final panel is saved to [data/final/final.csv](data/final/final.csv) with complete monthly observations where both climate and price data are available.



