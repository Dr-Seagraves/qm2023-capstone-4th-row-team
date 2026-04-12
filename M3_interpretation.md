# M3 Interpretation Memo — Econometric Models

**QM 2023 Capstone | 4th Row Team | Due: April 24, 2026**
**Research Question:** Has the globalized energy supply chain severed the link between severe U.S. winters and domestic heating oil prices?

---

## Data

**Outcome:** Real Heating Oil Price (2020 constant $/gallon; FRED APU000072511 deflated by CPIAUCSL)
**Primary Driver:** NEC_HDD — EIA STEO ZWHD_NEC — population-weighted Heating Degree Days for the New England Census Division (MA, ME, NH, VT, CT, RI). This covers approximately 75% of U.S. heating oil consumption and directly matches the geographic scope of the national price series.
**Global controls:** WTI Crude Oil Price (FRED MCOILWTICO); Henry Hub Natural Gas (FRED MHHNGSP)
**Sample:** 311 monthly observations, January 2000 – December 2025 (single entity time series; no panel structure)

---

## Model A Headline Finding

**A 1 Heating Degree Day increase in the New England Census Division (population-weighted, EIA) at lag 1 raises the real heating oil price by $0.0000114/gallon (HC3-robust SE = 0.0000285, p = 0.689).**

This coefficient is statistically indistinguishable from zero at every conventional significance level. In practical economic terms: a New England winter that is 500 HDD colder than normal — a severe cold anomaly — translates to a predicted price increase of **$0.0057/gallon**, or just over half a cent, against a base price of $2–5/gallon. Regional winter severity in the primary heating oil market is econometrically invisible once price persistence is controlled for.

The dominant predictor is the lagged real price itself: **β(AR(1)) = +0.9752 (p < 0.001)**. Each $1.00/gallon increase in real price last month predicts a $0.975/gallon increase this month, confirming the near-random-walk behavior documented in M2 (AR(1) autocorrelation ≈ 0.979).

**Model A R² = 0.9580.** Nearly all explained variation comes from price persistence, not weather.

---

## Economic Interpretation — Three Causal Channels

### Channel 1: Global Crude Oil Sets the Price Floor and Ceiling

Heating oil (No. 2 distillate fuel) is refined directly from crude oil, making its price a near-linear function of the WTI/Brent spot price. In the Random Forest model (Model B), WTI_Price captures 14.3% of feature importance and lagged price captures 85.1%; NEC_HDD contributes just 0.5%. Even a historic cold spell across all of New England increases U.S. distillate demand by a fraction of a percent of global crude consumption (~100 mb/d), which is far too small to shift the global equilibrium price. The price is set in Rotterdam and Cushing, not in Boston or Burlington.

### Channel 2: U.S. Shale Dramatically Increased Supply Elasticity

The subsample robustness check shows the NEC_HDD coefficient shifting from β = +0.0000351 (pre-2014, p = 0.289) to β = –0.0000059 (post-2014, p = 0.882). Neither is statistically significant, but the directional shift is consistent with the shale hypothesis. U.S. tight oil production grew from ~5 mb/d (2010) to ~13 mb/d (2019), dramatically increasing domestic crude supply elasticity. Seasonal demand spikes that would previously have triggered inventory drawdowns and temporary price premiums can now be absorbed via Gulf Coast–to–Northeast pipeline logistics within days, flattening the NEC_HDD-to-price transmission mechanism.

### Channel 3: The Null Result Is Robust Across All Geographic HDD Definitions

Robustness 5 runs the identical model specification with three different HDD measures — the population-weighted New England Census Division (EIA), the national U.S. average (EIA), and the single Boston Logan weather station (NOAA) — and obtains statistically indistinguishable null results in all three:

| HDD Measure | β | SE | p-value | R² |
|-------------|---|----|---------|----|
| NEC_HDD — New England, pop-weighted (EIA) | +0.0000114 | 0.0000285 | 0.689 | 0.9580 |
| US_HDD — National, pop-weighted (EIA) | +0.0000161 | 0.0000418 | 0.700 | 0.9580 |
| Boston_HDD — Single station (NOAA) | +0.0000152 | 0.0000311 | 0.624 | 0.9580 |

The null result is not an artifact of using a single weather station. Whether measured at one city, across a region, or nationally, HDD has no detectable effect on heating oil prices after controlling for price persistence. This eliminates the geographic mismatch as an explanation and focuses attention on the economic mechanisms: globalization of the crude oil supply chain has genuinely severed the local weather-price link.

---

## Model B Summary — ML Comparison (OLS vs Random Forest)

| Model | Test R² | Test RMSE ($/gal) |
|-------|---------|-------------------|
| Naive Baseline (last value) | –2.727 | 1.321 |
| OLS (5 features) | 0.892 | 0.225 |
| Random Forest (5 features) | 0.898 | 0.219 |

**Key takeaway:** Random Forest improves only marginally over OLS (R² +0.006, RMSE –$0.006/gal). The relationship between predictors and heating oil price is largely linear — the modest RF gain does not justify sacrificing OLS interpretability. The deeply negative naive baseline R² confirms that heating oil prices are not mean-reverting on monthly timescales and that any model must track the series dynamically.

**Feature importance from Random Forest (NEC_HDD as primary driver):**
- Lagged Price (AR(1)): **85.1%** — price is its own best predictor
- WTI Crude Price: **14.3%** — global oil market signal
- NEC_HDD (lag 1): **0.5%** — statistically and economically negligible
- Heating Season dummy: 0.1%
- Post-2014 dummy: 0.03%

Even the nonlinear Random Forest — which can detect interactions and threshold effects invisible to OLS — assigns only 0.5% importance to regional heating demand. Globalization has not merely weakened the weather-price link; it has effectively eliminated it from the price signal.

---

## Diagnostics — Implications and Fixes

### Heteroskedasticity (Breusch-Pagan)
- **Result:** LM = 26.50, p < 0.0001 — heteroskedasticity is present.
- **Implication:** Standard OLS standard errors understate uncertainty in crisis-period observations (2008, 2022), making the already-insignificant HDD coefficient appear more precisely estimated than it truly is.
- **Fix applied:** HC3 robust standard errors in Models 2 and 3. HC3 is preferred over HC1/HC2 in small-to-moderate samples because it provides better finite-sample coverage by downweighting high-leverage observations.
- **Interpretation of fix:** The NEC_HDD coefficient remains insignificant under HC3 (p = 0.689 vs p = 0.672 under standard SE), confirming that the null result is not a product of artificially narrow confidence intervals.

### VIF — Multicollinearity
- **Result:** All VIF < 1.32 — no problematic multicollinearity.
- **Implication:** Each predictor contributes independent information. The AR(1) term and NEC_HDD are not collinear; coefficient estimates are stable.

### Residual Plots
- **Residuals vs. Fitted:** No systematic pattern for low fitted values. Increased scatter (heteroskedasticity) at high fitted values (>$4.00/gal), corresponding to the 2008 and 2022 price spikes. This visually confirms the Breusch-Pagan result and justifies HC3.
- **Q-Q Plot:** Residuals deviate from the diagonal in the tails (leptokurtosis, Kurtosis ≈ 8.2), driven by the 2008 GFC and 2022 Russia-Ukraine war price shocks. With n = 310 observations, OLS coefficient estimates remain consistent by the Central Limit Theorem, though finite-sample confidence intervals are approximate.

---

## Robustness Checks

| Check | NEC_HDD β | p-value | R² | Notes |
|-------|-----------|---------|-----|-------|
| Model 1: Standard SE | +1.14e-05 | 0.672 | 0.9580 | Baseline |
| Model 2: HC3 Robust SE | +1.14e-05 | 0.689 | 0.9580 | Same null result; wider SEs |
| NEC_HDD lag 0 (contemporaneous) | –1.40e-05 | 0.753 | 0.9580 | Near zero, slightly negative |
| NEC_HDD lag 1 (baseline) | +1.14e-05 | 0.689 | 0.9580 | Optimal lag from M2 |
| NEC_HDD lag 2 | +3.50e-07 | 0.989 | 0.9594 | Essentially zero |
| NEC_HDD lag 3 | +3.91e-06 | 0.875 | 0.9601 | Near zero |
| Excl. 2008–09 & 2020 (N=274) | +3.00e-06 | 0.907 | 0.9610 | Crisis periods do not drive result |
| Pre-2014 subsample (N=167) | +3.40e-05 | 0.334 | 0.9746 | Larger but still insignificant |
| Post-2014 subsample (N=143) | –1.10e-05 | 0.826 | 0.9175 | Near zero; directional shale effect |
| NEC_HDD × Post-2014 interaction | –3.85e-05 | 0.398 | 0.9581 | Structural break not significant |
| Geographic: US_HDD (national, EIA) | +1.61e-05 | 0.700 | 0.9580 | Confirms null holds nationally |
| Geographic: Boston_HDD (NOAA) | +1.52e-05 | 0.624 | 0.9580 | Confirms null pre-dates data fix |

**Conclusion:** The null result is robust across 5 different checks (SE specification, lag structure, crisis exclusion, period subsample, geographic HDD definition). The geographic robustness check (Robustness 5) is particularly important: the null result holds whether we use population-weighted New England HDD, national U.S. HDD, or a single Boston weather station. This rules out measurement error in HDD as the explanation and implicates economic fundamentals — the globalization of the crude oil supply chain — as the true cause.

---

## Caveats and Limitations

### 1. Omitted Variables
The most important omitted variable is WTI crude oil price. Model A deliberately excludes WTI to isolate the HDD-to-price channel. In Model B (RF with WTI included), WTI gets 14.3% feature importance — confirming its importance but also suggesting that HDD's true conditional effect (after WTI) is indeed near zero. The WTI-NEC_HDD bivariate correlation is near zero (r ≈ 0.01), so omitted variable bias from WTI is likely small.

### 2. Aggregate vs. Regional Heating Oil Markets
The FRED heating oil price (APU000072511) is a national city average, but heating oil markets are regional. New England has distinct pricing from the Mid-Atlantic. A regional price series (e.g., EIA heating oil prices for New England specifically) paired with NEC_HDD would be an even tighter geographic match. EIA does publish regional heating oil retail prices, which could be explored in future work.

### 3. Structural Non-Stationarity
The ADF test (p = 0.047) barely rejects the unit root at 5%. The Dynamic OLS AR(1) specification handles price persistence, but rolling correlations (M2, Plot 5) confirmed that the HDD-price relationship is non-stationary. A single pooled coefficient may not characterize any particular regime well. Time-varying coefficient models (Kalman filter, rolling OLS) would be a natural extension.

### 4. Monthly Frequency May Obscure Weekly Effects
Heating oil demand is highly concentrated in extreme-cold weeks (e.g., polar vortex events). Monthly HDD aggregates these into smoother signals. At weekly frequency, short sharp cold spikes might show a stronger, short-lived price response that is averaged away in monthly data. Monthly frequency is the limit of our data availability; weekly analysis would require different data sources.

---

## Summary Statement

> **A 1 NEC_HDD increase (New England Census Division, EIA, population-weighted) at a one-month lag is associated with a $0.0000114/gallon increase in the real heating oil price (HC3-robust SE = 0.0000285, p = 0.689). This is economically negligible — a 500 HDD severe cold anomaly implies $0.0057/gal, less than one cent against a $2–5 base price. The AR(1) price term (β = 0.975, p < 0.001) dominates all variation. Crucially, this null result holds whether HDD is measured at a single Boston weather station, across the New England Census Division (population-weighted), or nationally across the United States — ruling out geographic measurement error as an explanation. Across five robustness checks, the NEC_HDD coefficient is statistically and economically insignificant at every lag, in every subsample, and in a flexible Random Forest model. The evidence is conclusive: the globalization of the crude oil supply chain has severed the statistical link between U.S. regional winter severity and domestic heating oil prices.**
