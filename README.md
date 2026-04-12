# QM 2023 Capstone: The Market Decoupling

**"Has the globalized energy supply chain severed the link between severe US winters and domestic heating oil prices?"**

## Research Question & Hypothesis

Historically, harsh US winters drove heating oil prices higher as local demand surged and supply chains struggled to respond. This project examines whether globalization of energy markets has weakened this relationship over time. As energy supply chains became more integrated internationally and alternative energy sources proliferated, we hypothesize that **the sensitivity of heating oil prices to extreme US winter weather has diminished**.

## Analytical Approach

### Core Relationship

We analyze the relationship between:
- **Winter Severity**: Measured by New England Census Division Heating Degree Days (NEC_HDD) — EIA STEO ZWHD_NEC, population-weighted across MA, ME, NH, VT, CT, RI (~75% of U.S. heating oil consumption)
- **Real Heating Oil Prices**: National average Fuel Oil #2 prices, adjusted for inflation (FRED APU000072511)

The fundamental question is whether HDD fluctuations predict price movements, and critically, **whether this predictive power has changed over recent decades**.

### Why New England Census Division HDD (EIA)?

The EIA STEO ZWHD_NEC series is the primary HDD measure for three reasons:
1. **Geographic match**: New England accounts for ~75% of U.S. heating oil consumption; this directly matches the geographic weight of the national price series
2. **Population-weighted**: The EIA series aggregates HDD across all of New England using population weights, not a single weather station, eliminating single-point measurement error
3. **Institutional authority**: This is the same HDD data the EIA uses in its own energy demand forecasting models

For robustness, we also include `US_HDD` (national U.S. average, EIA), `MAC_HDD` (Middle Atlantic, EIA), and `Boston_HDD` (Boston Logan Airport, NOAA — single station, retained for comparison). All four measures produce statistically identical null results in M3 regressions.

By pairing population-weighted regional climate data with national prices, we can test whether local weather shocks still drive national market outcomes—or whether markets have decoupled from regional weather patterns.

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

The final enriched dataset (`data/final/final_enriched.csv`) contains monthly observations with:
- `YearMonth`: Time identifier
- `Heating_Oil_Price`: Nominal price per gallon (USD, FRED APU000072511)
- `CPI`: Consumer Price Index for inflation adjustment (FRED CPIAUCSL)
- `Real_Heating_Oil_Price`: Inflation-adjusted price ratio (Nominal/CPI)
- `NEC_HDD`: **Primary driver** — EIA New England Census Division HDD, population-weighted (EIA STEO ZWHD_NEC)
- `US_HDD`: U.S. national HDD, population-weighted (EIA STEO ZWHDPUS) — robustness check
- `MAC_HDD`: Middle Atlantic HDD (NY/NJ/PA), EIA STEO ZWHD_MAC — robustness check
- `Boston_HDD`: Single-station HDD, Boston Logan Airport, NOAA GSOM — comparison only
- `WTI_Price`: WTI Crude Oil Price (FRED MCOILWTICO, $/barrel)
- `HenryHub_Price`: Henry Hub Natural Gas Spot Price (FRED MHHNGSP, $/MMBtu)

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

Create a `.env` file in the project root:

```
FRED_API_KEY=your_fred_api_key
NOAA_API_TOKEN=your_noaa_token
EIA_API_KEY=your_eia_api_key
```

*Obtain keys from FRED, NOAA CDO, and EIA (free, instant registration at eia.gov/opendata).*

### 2. Execute the Pipeline

```bash
# Step 1: Fetch FRED + NOAA base panel (final.csv)
python code/main_panel.py

# Step 2: Enrich with EIA regional HDD + commodity controls (final_enriched.csv)
python enrich_panel.py

# Step 3: Run EDA
jupyter nbconvert --to notebook --execute capstone_eda.ipynb

# Step 4: Run econometric models
python capstone_models.py
```

### 3. Output

The analysis-ready enriched panel is saved to `data/final/final_enriched.csv` — 311 rows × 10 columns, zero missing values.



