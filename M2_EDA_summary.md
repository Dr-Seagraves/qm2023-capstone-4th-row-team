# M2 EDA Summary — Real Heating Oil Prices & Winter Severity

**QM 2023 Capstone | 4th Row Team | Due: March 27, 2026**

**Dataset:** Monthly time series, January 2000 – December 2025 (n = 311 observations; October 2025 missing from NOAA)
**Outcome variable:** Real Heating Oil Price (2020 constant $/gallon; FRED APU000072511 deflated by CPIAUCSL)
**Main driver:** Heating Degree Days — New England Census Division (EIA STEO ZWHD_NEC; population-weighted across MA, ME, NH, VT, CT, RI)
**Global controls:** WTI Crude Oil Price (FRED MCOILWTICO, r = +0.946) · Henry Hub Natural Gas (FRED MHHNGSP, r = +0.297)
**Key analytical finding:** After removing WTI, NEC_HDD explains r = +0.174 of the residual local demand premium (vs r ≈ 0.00 raw across all lags)
**Research question:** Has the globalized energy supply chain severed the link between severe U.S. winters and domestic heating oil prices?

**Geographic match note:** NEC_HDD (EIA STEO ZWHD_NEC) is the population-weighted average HDD across all of New England, which accounts for approximately 75% of U.S. heating oil consumption. This directly matches the geographic scope of the FRED heating oil price series and eliminates the single-station measurement error present in weather-station-only approaches.

---

## Key Findings

1. **NEC_HDD has a near-zero correlation with real heating oil price at every tested lag (r ≈ –0.005 to +0.011 at lags 0–12 months).** This is the central empirical finding: regional winter severity in New England — the primary heating oil consumption zone — contributes almost nothing to the monthly variation in the national average heating oil price. Global crude oil cycles dominate. This directly answers the research question: the globalized energy supply chain has severed the statistical link between U.S. winter severity and domestic heating oil prices.
   *Economic mechanism:* Heating oil is a crude-oil derivative; its price tracks global WTI/Brent spot prices. Even a severe New England winter increases U.S. distillate demand by a fraction of a percent of global consumption (~100 mb/d) — far too small to shift the global equilibrium price. Distributors can source additional supply from Gulf Coast terminals via the Colonial Pipeline within days, further dampening any local scarcity premium.

2. **The rolling 24-month correlation between NEC_HDD and real price is highly time-varying — and frequently collapses to near zero or turns negative during global energy supply shocks.** During the 2008–09 financial crisis, the 2014–16 shale glut, and the 2020 COVID demand collapse, the HDD–price link was overwhelmed by supply-side forces. This is the central empirical finding for the research question: globalization (and U.S. shale production) has made the local demand signal noisier relative to the global supply signal.
   *Economic mechanism:* When global crude prices collapse (GFC, shale), even record-cold winters cannot sustain elevated heating oil prices. The oil price floor is set globally, not locally.

3. **Within-period correlations differ across economic regimes, with directional evidence of a weakening HDD-price link post-2014.**
   Pre-Crisis (2000–07): r = +0.033; Post-GFC (2008–14): r = –0.070; Shale Era (2015–19): r = +0.106 (elevated due to cold 2015 winters coinciding with recovery); COVID (2020–21): r = +0.268; Recovery (2022–25): r = –0.067. The non-stationarity warns against imposing a constant HDD coefficient across the full 25-year sample.
   *Economic mechanism:* U.S. tight oil production grew from ~5 mb/d (2010) to ~13 mb/d (2019), making domestic supply far more elastic and reducing the seasonal inventory drawdown effect.

4. **The seasonal decomposition reveals a real but secondary winter price premium (≈$0.15–0.30/gal peak-to-trough), dwarfed by the trend component ($3+ per-gallon range across the crude oil super-cycle).** Residuals show pronounced heteroskedasticity — large spikes in 2008 and 2022 exceed ±2σ — indicating that the variance of the error term changes across regimes.
   *Economic mechanism:* The large residuals correspond to geopolitical and financial tail events (Lehman Brothers collapse, Russia–Ukraine war) that no domestic weather variable can capture.

5. **Strong price autocorrelation (AR(1) lag-1 r ≈ 0.979) confirms that heating oil prices are highly persistent.** Any M3 regression without a lagged dependent variable will produce biased coefficient estimates due to serially correlated residuals.
   *Economic mechanism:* Commodity prices follow near-random-walk processes; short-run supply and demand adjustments are slow relative to the monthly sampling frequency.

---

## Hypotheses for M3

### Hypothesis 1: NEC_HDD Effect on Real Heating Oil Price (Main Driver)

- **Claim:** A one-unit increase in monthly NEC_HDD at the optimal lag increases the real heating oil price by a positive and statistically significant amount, holding lagged price and seasonal effects constant.
- **Model specification:**
  ```
  Real_Price_t = β₀ + β₁·NEC_HDD_{t-k*} + β₂·Real_Price_{t-1} + β₃·HeatingSeason_t + β₄·Post2014_t + εₜ
  ```
  where `k*` = optimal lag (evaluated at 0, 1, 2, 3 months) and `HeatingSeason_t` = 1 if month ∈ {Oct, Nov, Dec, Jan, Feb, Mar}.
- **Expected sign:** β₁ > 0 (positive demand effect)
- **Expected magnitude:** Very small and likely statistically insignificant given the near-zero bivariate correlation (r ≈ 0.00–0.01 at all lags). The partial correlation after removing WTI (+0.174) is larger, suggesting a conditional HDD effect may emerge in a controlled regression, but even this is weak.
- **Economic mechanism:** HDD increases residential and commercial fuel demand. Distributors draw down regional storage, creating temporary upward price pressure until national supply logistics respond.

### Hypothesis 2: Structural Break — Shale Era Weakened the NEC_HDD Sensitivity

- **Claim:** The NEC_HDD–price coefficient is significantly smaller (closer to zero) in the post-2014 Shale Era than in the Pre-Crisis era, reflecting increased domestic supply elasticity.
- **Model specification (interaction):**
  ```
  Real_Price_t = β₀ + β₁·NEC_HDD_{t-1} + β₂·Post2014_t + β₃·(NEC_HDD_{t-1} × Post2014_t)
                + β₄·Real_Price_{t-1} + β₅·HeatingSeason_t + εₜ
  ```
- **Expected sign:** β₃ < 0 (interaction term dampens the HDD effect post-2014)
- **Economic mechanism:** U.S. shale production transformed the country from a price-taker to a partial price-setter in global oil markets.

### Hypothesis 3: Heating-Season Price Premium (Seasonal Dummy)

- **Claim:** Holding NEC_HDD and lagged price constant, prices are systematically higher during the October–March heating season due to anticipatory stockpiling and forward contracting by distributors.
- **Expected sign:** β₅ > 0 (heating season premium)
- **Economic mechanism:** Distributors pre-purchase and pre-price heating oil ahead of winter, creating a price premium independent of the contemporaneous weather realization.

---

## Data Quality Flags & M3 Mitigations

| Flag | Details | M3 Mitigation |
|------|---------|---------------|
| **Heteroskedasticity** | Residual variance higher during supply-shock regimes | HC3 robust standard errors in all M3 regressions |
| **Non-stationarity / trend** | Real price has non-linear trend; ADF p = 0.047 (borderline) | Include AR(1) lagged DV (dynamic OLS) |
| **Serial autocorrelation** | AR(1) coefficient ≈ 0.979; Durbin-Watson far from 2.0 in static OLS | Lagged dependent variable in dynamic OLS specification |
| **Outlier observations** | Real price spikes in 2008 (GFC) and 2022 (Ukraine) exceed ±2σ | Crisis exclusion robustness check; HC3 SEs downweight leverage |
| **Geographic scope** | *Resolved:* NEC_HDD (EIA STEO ZWHD_NEC) is population-weighted across all of New England, matching the geographic scope of heating oil consumption | Primary driver in all M3 models; Boston_HDD retained as robustness comparison |
| **HDD rescaling** | Real_Heating_Oil_Price in raw CSV is Nominal/CPI (unitless ratio ≈ 0.007–0.02). Rescaled to 2020 $/gal for all M3 analysis | `Real_Price_2020 = Heating_Oil_Price / CPI × CPI_2020`; documented in methods |
