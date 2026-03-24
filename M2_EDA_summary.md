# M2 EDA Summary — Real Heating Oil Prices & Winter Severity

**QM 2023 Capstone | 4th Row Team | Due: March 27, 2026**

**Dataset:** Monthly panel, January 2000 – December 2025 (n = 311 observations; October 2025 missing from NOAA)
**Outcome variable:** Real Heating Oil Price (2020 constant $/gallon, FRED APU000072511 × CPI)
**Main driver:** Heating Degree Days — Boston Logan Airport (NOAA GSOM, WBAN:14739)
**Global controls:** WTI Crude Oil Price (FRED MCOILWTICO, r = +0.94) · Henry Hub Natural Gas (FRED MHHNGSP, r = +0.30)
**Key analytical finding:** After removing WTI, HDD explains r = +0.28 of the residual local demand premium (vs r ≈ 0.00 raw)
**Research question:** Has the globalized energy supply chain severed the link between severe U.S. winters and domestic heating oil prices?

---

## Key Findings

1. **HDD has a near-zero correlation with real heating oil price at every tested lag (r ≈ –0.03
   to +0.01 at lags 0–12 months).** This is the central empirical finding: local winter severity
   at Boston Logan contributes almost nothing to the monthly variation in the national average
   heating oil price. Global crude oil cycles dominate. This directly answers the research
   question — the globalized energy supply chain has effectively severed the statistical link
   between Boston-area winters and domestic heating oil prices.
   *Economic mechanism:* Heating oil is a crude-oil derivative; its price tracks global WTI/Brent
   spot prices. A cold week in New England increases regional distillate demand by a fraction of
   a percent of global consumption — far too small to move the global price. Distributors can
   also source additional supply from national pipelines and terminals within days, further
   dampening any local scarcity premium.

2. **The rolling 24-month correlation between HDD and real price is highly time-varying — and
   frequently collapses to near zero or turns negative during global energy supply shocks.**
   During the 2008–09 financial crisis, the 2014–16 shale glut, and the 2020 COVID demand
   collapse, the HDD–price link was overwhelmed by supply-side forces. This is the central
   empirical finding for the research question: globalization (and U.S. shale production)
   has made the local demand signal noisier relative to the global supply signal.
   *Economic mechanism:* When global crude prices collapse (GFC, shale), even record-cold winters
   cannot sustain elevated heating oil prices. The oil price floor is set globally.

3. **Within-period correlations differ significantly across economic regimes.**
   The Pre-Crisis era (2000–07) shows the strongest positive HDD–price correlation, while
   Post-GFC and Shale Era periods show weaker or near-zero correlations. This non-stationarity
   implies a structural break around 2008 (GFC) and potentially 2014 (shale revolution), and
   warns against imposing a constant HDD coefficient across the full 25-year sample.
   *Economic mechanism:* U.S. tight oil production grew from ~5 mb/d (2010) to ~13 mb/d (2019),
   making domestic supply far more elastic and reducing the seasonal inventory drawdown effect.

4. **The seasonal decomposition reveals a real but secondary winter price premium (≈$0.15–0.30/gal
   peak-to-trough), dwarfed by the trend component ($3+ per-gallon range across the super-cycle).**
   Residuals show pronounced heteroskedasticity — large spikes in 2008 and 2022 exceed ±2σ —
   indicating that the variance of the error term changes across regimes.
   *Economic mechanism:* The large residuals correspond to geopolitical and financial tail events
   (Lehman Brothers collapse, Russia–Ukraine war) that no domestic weather variable can capture.

5. **Strong price autocorrelation (AR(1) lag-1 r ≈ 0.95+) confirms that heating oil prices are
   highly persistent.** Any M3 regression without a lagged dependent variable will produce
   spurious or biased coefficient estimates due to serially correlated residuals.
   *Economic mechanism:* Commodity prices follow near-random-walk processes; short-run supply
   and demand adjustments are slow relative to the monthly sampling frequency.

---

## Hypotheses for M3

### Hypothesis 1: HDD Effect on Real Heating Oil Price (Main Driver)

- **Claim:** A one-unit increase in monthly HDD at the optimal lag increases the real heating oil
  price by a positive and statistically significant amount, holding lagged price and seasonal
  effects constant.
- **Model specification:**
  ```
  Real_Price_t = β₀ + β₁·HDD_{t-k*} + β₂·Real_Price_{t-1} + β₃·HeatingSeason_t + ε_t
  ```
  where `k*` = optimal lag from Plot 4, and `HeatingSeason_t` = 1 if month ∈ {Oct, Nov, Dec, Jan, Feb, Mar}.
- **Expected sign:** β₁ > 0 (positive demand effect)
- **Expected magnitude:** Likely very small and possibly statistically insignificant given the
  near-zero bivariate correlation (r ≈ 0.00–0.01). Any detectable HDD effect may only emerge
  after conditioning on regime dummies and price persistence — conditional on a stable global
  supply environment, local demand shocks may matter at the margin.
- **Economic mechanism:** HDD increases residential and commercial fuel demand. Distributors draw
  down local storage, creating a temporary upward price pressure until national supply logistics respond.

### Hypothesis 2: Structural Break — Shale Era Weakened the HDD Sensitivity

- **Claim:** The HDD–price coefficient is significantly smaller (closer to zero) in the post-2014
  Shale Era than in the Pre-Crisis era, reflecting increased domestic supply elasticity.
- **Model specification (Chow test / interaction):**
  ```
  Real_Price_t = β₀ + β₁·HDD_{t-k*} + β₂·Post2014_t + β₃·(HDD_{t-k*} × Post2014_t)
                + β₄·Real_Price_{t-1} + β₅·HeatingSeason_t + ε_t
  ```
- **Expected sign:** β₃ < 0 (the interaction term dampens the HDD effect post-2014)
- **Test:** Chow test for structural break at 2014-Q4; also test breakpoint at 2008-Q4.
- **Economic mechanism:** U.S. shale production transformed the country from a price-taker to a
  partial price-setter in global oil markets. Increased spare capacity means that seasonal demand
  spikes are absorbed at lower marginal cost, flattening the HDD slope.

### Hypothesis 3: Heating-Season Price Premium (Seasonal Dummy)

- **Claim:** Holding HDD and lagged price constant, prices are systematically higher during the
  October–March heating season due to anticipatory stockpiling and forward contracting by distributors.
- **Model specification:** Binary variable `HeatingSeason_t` in the baseline regression.
- **Expected sign:** β₅ > 0 (heating season premium)
- **Economic mechanism:** Distributors and utilities pre-purchase and pre-price heating oil ahead
  of the winter season. This anticipatory behavior creates a price premium independent of the
  contemporaneous weather realization, captured by the seasonal dummy rather than by HDD directly.

---

## Data Quality Flags & M3 Mitigations

| Flag | Details | M3 Mitigation |
|------|---------|---------------|
| **Outlier observations** | Real price spikes in 2008 (GFC) and 2022 (Ukraine war) exceed ±2σ of residuals; distorts OLS estimates | Add `Crisis_Dummy` (= 1 for 2008–09 and 2022–23); consider robust regression (M-estimator) |
| **Heteroskedasticity** | Residual variance is higher during supply-shock regimes (confirmed by decomposition and visual inspection) | Use HC3 (heteroskedasticity-consistent) robust standard errors in all M3 regressions |
| **Non-stationarity / trend** | Real price series has a strong non-linear trend (rising to 2008, falling, rising again) | Include year trend or first-difference specification; test for unit root (ADF) before OLS |
| **Multicollinearity** | Year and CPI are correlated (~0.9+); both capture the secular price trend | Drop CPI from M3 (already used to construct the outcome variable); keep Year as trend proxy |
| **Serial autocorrelation** | AR(1) coefficient ≈ 0.95; Durbin-Watson will be far from 2.0 in static OLS | Include lagged dependent variable (dynamic OLS) or use Newey-West standard errors |
| **Single geographic station** | HDD from Boston Logan only — may not represent national heating demand | Note as study limitation; the national FRED price series and single-city HDD measure creates a **mismatch in geographic scope** that attenuates the estimated coefficient (measurement error in X) |
| **HDD rescaling** | Real_Heating_Oil_Price in the raw dataset is Nominal/CPI (unitless ratio ≈ 0.007–0.02). We rescale to 2020 constant $/gal for interpretability. Both measures are included in the heatmap for transparency. | Document the rescaling formula in the methods section of M3 |
