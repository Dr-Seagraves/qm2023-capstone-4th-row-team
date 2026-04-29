# MEMORANDUM

**TO:** Investment Committee, Energy Commodities Division
**FROM:** 4th Row Team — Matthew Talburt, Joshua Keoshkarian, Jeret Stone, Cooper Worsham
**DATE:** May 1, 2026
**RE:** Heating Oil Price Sensitivity to Winter Severity — Has Globalization Ended Weather-Driven Price Risk?

---

## I. Executive Summary

Over the past 26 years, the U.S. heating oil market has undergone a fundamental structural transformation. Using 311 monthly observations from January 2000 through December 2025, we find that severe New England winters — the primary heating oil consumption zone — have **no statistically detectable effect on the national average heating oil price**, after accounting for price persistence. A winter that is 500 Heating Degree Days colder than average (a historically severe anomaly roughly equivalent to the 2014 polar vortex) translates to a predicted price increase of **$0.006 per gallon** — less than one-quarter of one percent on a $2.50 base price. The dominant driver of price is last month's price itself (AR(1) coefficient = 0.975), indicating that heating oil prices behave like a near-random walk anchored to global crude oil markets, not regional weather cycles.

The practical implication for portfolio management is straightforward: **weather-based price forecasts, heating-degree-day derivatives, and seasonal long positions in heating oil futures are unlikely to generate alpha.** Heating oil is priced in Rotterdam and Cushing, not Burlington or Boston. Even a record-cold New England winter increases U.S. distillate demand by a fraction of one percent of global crude consumption (~100 million barrels per day) — a shock far too small to move a global market price. The shale revolution (post-2014) amplified this dynamic further, making domestic supply highly elastic and allowing Gulf Coast refiners to route additional supply to the Northeast within days.

Our recommendation to the Investment Committee is to **redirect weather-monitoring and weather-derivative budget toward global crude oil signal analysis.** WTI crude oil prices carry a 0.946 correlation with real heating oil prices — more than 700 times the explanatory power of any weather variable we tested. Three forward-looking scenarios (see Section IV) illustrate that the dominant source of price risk over the next 12 months is geopolitical supply disruption in crude oil markets, not winter severity. A crude oil supply shock of +$20/bbl implies a heating oil price increase of approximately $0.60/gallon (+24%); a polar vortex winter implies an increase of $0.006/gallon (<1%). Hedging strategy should reflect this asymmetry.

---

## II. Methodology

### 2.1 Data Sources

**Primary Dataset — Heating Oil Prices**
- **Source:** Federal Reserve Economic Data (FRED), Series APU000072511 — U.S. City Average Price, No. 2 Heating Oil
- **Coverage:** 311 monthly observations, January 2000 – December 2025
- **Variable:** Nominal price deflated by CPIAUCSL (Consumer Price Index, All Urban Consumers) to produce real 2020 constant $/gallon

**Weather Data — Heating Degree Days**
- **Source:** U.S. Energy Information Administration (EIA), Short-Term Energy Outlook (STEO), Series ZWHD_NEC — New England Census Division HDD
- **Rationale:** Population-weighted average across MA, ME, NH, VT, CT, and RI — covering approximately 75% of U.S. heating oil consumption. This directly matches the geographic scope of the FRED price series.
- **Robustness:** U.S. national HDD (EIA ZWHDPUS) and Boston Logan single station (NOAA GSOM) used as alternative HDD measures in robustness checks.

**Global Control Variable**
- **Source:** FRED, Series MCOILWTICO — WTI Crude Oil Price ($/barrel)
- **Use:** Included in Model B only; excluded from Model A to isolate the direct weather-to-price channel

**CPI Deflator**
- **Source:** FRED, Series CPIAUCSL (Base Year 2015=100; rescaled to 2020 average = 1.0)

### 2.2 Sample Construction

| Step | Observations |
|------|-------------|
| FRED heating oil price series (start: Nov 1978) | 565 |
| Intersect with NOAA/EIA HDD data (start: Jan 2000) | 312 |
| Drop October 2025 (NOAA station gap, documented) | 311 |
| Drop first row for AR(1) lag construction | **310 modeling observations** |

**Panel structure:** Single entity (U.S. national), monthly frequency, January 2000 – December 2025. No missing values in final sample (confirmed: `df.isna().sum() == 0`). Because our dataset is a single time series — not a multi-entity panel — entity fixed effects are not applicable. Dynamic OLS with a lagged dependent variable is the correct single-entity analogue to Fixed Effects.

### 2.3 Model Specifications

**Model A — Dynamic OLS (Primary Causal Model)**

$$\text{Real\_Price}_t = \beta_0 + \beta_1 \cdot \text{Real\_Price}_{t-1} + \beta_2 \cdot \text{NEC\_HDD}_{t-1} + \beta_3 \cdot \text{HeatingSeason}_t + \beta_4 \cdot \text{Post2014}_t + \varepsilon_t$$

Where:
- $\text{Real\_Price}_t$: Real heating oil price in 2020 constant $/gallon
- $\text{Real\_Price}_{t-1}$: AR(1) lagged dependent variable (absorbs price persistence; AR(1) autocorrelation = 0.979)
- $\text{NEC\_HDD}_{t-1}$: Population-weighted New England Heating Degree Days at one-month lag
- $\text{HeatingSeason}_t$: Binary indicator, 1 for October–March
- $\text{Post2014}_t$: Binary indicator, 1 for January 2014 onward (captures shale era structural break)
- Standard errors: HC3 heteroskedasticity-robust (Breusch-Pagan: LM = 26.50, p < 0.001 — heteroskedasticity confirmed) and Newey-West HAC (bandwidth = 12 months; corrects for mild residual serial correlation, DW = 1.27)

**Model B — OLS vs. Random Forest (Predictive Comparison)**
- Features: AR(1) price, NEC_HDD (lag 1), WTI crude price, Heating Season, Post-2014
- Chronological 80/20 train/test split: training on Jan 2000 – Sep 2020 (248 obs), testing on Oct 2020 – Dec 2025 (62 obs)
- Goal: Assess whether nonlinear ML or including WTI changes the null result for HDD

---

## III. Results

### 3.1 Model A — Dynamic OLS Regression Results

**Table 1: Real Heating Oil Price — Dynamic OLS (HC3 Robust Standard Errors)**

| Variable | Coefficient | HC3 Std. Error | t-statistic | p-value | Significance |
|----------|-------------|----------------|-------------|---------|--------------|
| Real Price (t−1) | 0.9752 | 0.0159 | 61.3 | <0.001 | *** |
| NEC_HDD (lag 1, $/gal per HDD) | 1.14 × 10⁻⁵ | 2.85 × 10⁻⁵ | 0.40 | 0.689 | — |
| Heating Season (Oct–Mar = 1) | See full table† | — | — | — | — |
| Post-2014 Dummy (shale era) | See full table† | — | — | — | — |
| Constant | See full table† | — | — | — | — |
| **Observations** | **310** | | | | |
| **R²** | **0.9580** | | | | |
| **Adjusted R²** | **0.9574** | | | | |
| **SE type** | **HC3 Robust** | | | | |

*Note: *** p < 0.01. Full coefficient table available in `results/tables/M3_regression_table_detailed.csv`. Newey-West HAC (lag-12) results yield p > 0.689 for NEC_HDD — null confirmed under serial-correlation correction.*

†*Control variable coefficients available in the repository regression table. All controls function as designed: the heating season dummy captures residual seasonal premium after AR(1); the Post-2014 dummy captures the structural price decline following the 2014 shale glut. Neither alters the null result for NEC_HDD.*

**Key finding:** The NEC_HDD coefficient of +1.14 × 10⁻⁵ dollars per gallon per Heating Degree Day is statistically indistinguishable from zero at every conventional significance level (p = 0.689). In plain terms: **a New England winter 500 HDD colder than average — historically a severe event — predicts a heating oil price increase of $0.006 per gallon.** On a typical price of $2.50 per gallon, this is a 0.2% change, within the measurement noise of the price series itself.

The AR(1) coefficient of 0.9752 tells a completely different story: this month's price is 97.5 cents for every dollar of last month's price. **Price history — not winter forecasts — is the only reliable predictor.**

### 3.2 Model A vs. Model B — Comparison Table

**Table 2: Model Comparison — Causal OLS vs. Predictive OLS vs. Random Forest**

| Metric | Model A: Dynamic OLS (Causal) | Model B: OLS + WTI (Predictive) | Model B: Random Forest |
|--------|-------------------------------|----------------------------------|------------------------|
| Purpose | Causal inference | Predictive accuracy | Nonlinear benchmark |
| Key variables | AR(1), NEC_HDD, Season, Post2014 | Same + WTI price | Same 5 features |
| Observations | 310 (full sample) | 248 train / 62 test | 248 train / 62 test |
| In-sample R² | 0.9580 | 0.9886 | N/A |
| Out-of-sample R² | N/A | **0.892** | **0.898** |
| Test-set RMSE | N/A | $0.225/gal | $0.219/gal |
| AR(1) weight | 0.9752*** | 0.622*** | 85.1% importance |
| NEC_HDD weight | p = 0.689 (not sig.) | Near zero | **0.5% importance** |
| WTI weight | Excluded | 0.030*** | 14.3% importance |
| Causal interpretation | Yes | Limited | No |

**Key takeaway:** Even a flexible nonlinear Random Forest assigns only 0.5% importance to weather. Adding WTI to the model reduces the AR(1) coefficient from 0.975 to 0.622 — confirming that crude oil absorbs the same global supply signal that makes prices so persistent. HDD's importance is negligible in both the causal model and the predictive model.

### 3.3 Figure Descriptions

**Figure 1 — Rolling 24-Month Correlation: NEC_HDD vs. Real Price**
*(File: `results/figures/plot5_rolling_correlation_comparison.png`)*

The rolling 24-month correlation between New England winter severity (NEC_HDD) and real heating oil prices fluctuates between −0.35 and +0.35 over the 2000–2025 period, with no stable positive relationship at any point. During the 2008–09 global financial crisis and the 2014–16 shale price collapse, the correlation turned sharply negative — severe winters coincided with collapsing oil prices driven entirely by global supply shocks. This visual confirms that weather does not cause prices: the relationship is overwhelmed by global crude market forces in every economic regime. The dual-axis time series (Plot 3) shows this directly: oil price macro-cycles (×$3 range) dwarf any weather-driven variation.

**Figure 2 — Residuals vs. Fitted Values (Diagnostic)**
*(File: `results/figures/M3_residuals_vs_fitted.png`)*

The residual scatter is centered at zero with no systematic pattern for fitted values below $4.00/gallon, confirming the linear specification is appropriate for the bulk of the sample. At fitted values above $4.00/gallon — corresponding to the 2008 GFC and 2022 Russia–Ukraine war price spikes — variance fans out noticeably, confirming heteroskedasticity (Breusch-Pagan p < 0.001) and justifying the HC3 and Newey-West standard error corrections applied to all inference. The Q-Q plot shows leptokurtosis (kurtosis ≈ 8.2) in the tails, consistent with rare geopolitical price shocks that a time-series model cannot anticipate.

### 3.4 Robustness Summary

The null result for NEC_HDD is confirmed across all five robustness checks and two additional bonus checks:

| Check | NEC_HDD p-value | Conclusion |
|-------|-----------------|------------|
| Standard OLS (baseline) | 0.672 | Null holds |
| HC3 Robust SE (preferred) | 0.689 | Null holds |
| **Newey-West HAC SE (Bonus)** | **> 0.689** | **Null holds under serial-correlation correction** |
| Lag 0 (contemporaneous) | 0.753 | Null holds |
| Lag 2 | 0.989 | Null holds |
| Lag 3 | 0.875 | Null holds |
| Exclude 2008–09 & 2020 crises | 0.907 | Not a crisis artifact |
| Pre-2014 subsample | 0.334 | Larger but still insignificant |
| Post-2014 subsample | 0.826 | Near zero; shale effect directionally visible |
| Geographic: U.S. national HDD | 0.700 | Null holds nationally |
| Geographic: Boston single station | 0.624 | Null predates geographic fix |
| Bootstrap 95% CI (Bonus) | Spans zero | Model-free confirmation |

---

## IV. Conclusions & Recommendations

### 4.1 Core Investment Recommendation

The evidence is unambiguous: **weather is not a useful signal for heating oil price direction.** Three economic channels explain why:

1. **Global crude sets the price floor.** Heating oil is a refined crude oil product. Its price is determined in global futures markets (Rotterdam, Cushing), not by regional demand shocks. A New England demand spike represents at most 0.05% of global daily consumption — far below any market-moving threshold.

2. **Shale production made U.S. supply highly elastic.** Post-2014, U.S. tight oil production grew from 5 mb/d to 13 mb/d, giving refiners the logistical capacity to route supply to any regional shortage within days. The shale era has effectively converted the Northeast from a supply-constrained heating oil market into one connected to the global crude grid.

3. **Price follows a near-random walk (AR(1) = 0.975).** The best 30-day forecast of the heating oil price is simply today's price. Short-term weather forecasts do not improve on this baseline.

**Specific recommendation:** Redirect seasonal weather-derivative hedging budget toward crude oil price risk management. A $10/bbl move in WTI implies a ~$0.30/gal move in heating oil — 50 times the impact of a major cold weather anomaly. Portfolio managers holding heating oil exposure should monitor WTI/Brent spreads and OPEC production policy, not the National Weather Service extended forecast.

### 4.2 Scenario Analysis (Bonus: 3+ Scenarios with Probability Weights)

The table below quantifies expected 12-month heating oil price changes under five forward-looking scenarios, based on our model's estimated channels.

**Table 3: 12-Month Price Scenario Analysis**

| Scenario | Probability | Primary Driver | Weather Channel Impact | Crude Oil Channel Impact | Expected Price Change |
|----------|-------------|----------------|-----------------------|--------------------------|-----------------------|
| **Geopolitical crude shock** (Russia/OPEC supply cut) | 15% | Global supply disruption | +$0.006/gal (+500 HDD anomaly, if any) | +$20/bbl WTI → +$0.60/gal | **+24%** |
| **Demand-driven crude rally** (China/India demand surge) | 20% | Global demand recovery | None | +$10/bbl WTI → +$0.30/gal | **+12%** |
| **Status quo** (near-random walk, no major shock) | 40% | AR(1) persistence | Negligible | Negligible | **~0%** |
| **Polar vortex event** (500 HDD above normal) | 10% | Severe cold anomaly | +$0.006/gal | None (independently) | **<1%** |
| **Mild recession** (demand destruction, crude weakness) | 15% | Global demand contraction | None | −$15/bbl WTI → −$0.45/gal | **−18%** |
| **Probability-weighted expected change** | **100%** | | | | **+3.4%** |

*Calculation: 0.15×(+24%) + 0.20×(+12%) + 0.40×(0%) + 0.10×(<1%) + 0.15×(−18%) = 3.6% + 2.4% + 0.1% + 0% − 2.7% = **+3.4%***.

**Reading this table:** The polar vortex scenario — historically the central concern of heating oil risk managers — contributes less than 0.1 percentage points to the probability-weighted expected price change. The geopolitical shock scenario alone contributes 3.6 percentage points. This asymmetry directly quantifies the reallocation argument: **hedging weather risk in heating oil is mispriced relative to the actual distribution of price risks.**

### 4.3 External Validation Against 2020–2025 Actual Prices (Bonus)

Model B was trained exclusively on 2000–2020 data and evaluated on an out-of-sample test period spanning October 2020 through December 2025 (62 months). This test period includes the COVID demand collapse (2020–21), the 2022 Russia-Ukraine war supply shock (WTI to $130/bbl), and the 2023–2025 price normalization — three distinct and unprecedented regimes not present in the training data. Despite this, the OLS model achieved:

- **Out-of-sample R² = 0.892** (explains 89% of real price variation in 2020–2025)
- **RMSE = $0.225/gallon** (average forecast error under $0.25 across the full test period)
- **Random Forest R² = 0.898**, RMSE = $0.219 — marginal improvement confirms linearity assumption is appropriate

The AR(1) structure generalizes across all three out-of-sample regimes without retraining. NEC_HDD contributes 0.5% of Random Forest feature importance in the test period — consistent with the full-sample result. The model's strong out-of-sample performance validates both the AR(1) specification and the null result for weather.

### 4.4 Caveats and Limitations

**1. National average price vs. regional New England prices.** FRED APU000072511 is a U.S. national city average, while NEC_HDD measures a regional variable. New England heating oil prices historically carry a geographic premium due to limited pipeline infrastructure. A fully matched regional price series (EIA State Energy Data System — MA, CT, RI) paired with NEC_HDD would provide an even tighter test of the local demand-price link. The geographic mismatch, if anything, biases against finding a null result — the actual local premium is likely even smaller than our estimate suggests.

**2. Monthly frequency may obscure short-lived polar vortex effects.** Heating oil demand is highly concentrated in extreme-cold weeks. Monthly HDD aggregates suppress the within-month volatility of a 72-hour polar vortex event. At weekly frequency, a short sharp cold spike might produce a detectable but short-lived price response that averages away in monthly data. Weekly data would be required to test this hypothesis.

**3. Borderline stationarity.** The Augmented Dickey-Fuller test barely rejects a unit root at 5% (p = 0.047), and the Durbin-Watson statistic (1.27) indicates mild residual serial correlation after the AR(1) correction. We applied Newey-West HAC standard errors (bandwidth = 12 months) to address this; the null result holds under all SE specifications. Time-varying coefficient models (Kalman filter, rolling OLS with adaptive bandwidth) would be a natural extension to test whether the HDD effect varies across short windows.

**4. The null result does not imply zero seasonal pattern.** The seasonal decomposition (M2 Plot 8) shows a real but secondary winter price premium of $0.15–0.30/gallon peak-to-trough. Our null result specifically addresses whether deviations from the seasonal average — i.e., whether a colder-than-normal winter — move prices beyond what the AR(1) predicts. The answer is no; the seasonal pattern is priced in through the HeatingSeason dummy, not through HDD variation.

---

## V. References

Hamilton, J.D. (1994). *Time Series Analysis*. Princeton University Press. (Chapter 17: AR specifications for commodity prices.)

Long, J.S., & Ervin, L.H. (2000). Using Heteroscedasticity Consistent Standard Errors in the Linear Regression Model. *The American Statistician*, 54(3), 217–224. (Basis for HC3 SE selection.)

Newey, W.K., & West, K.D. (1987). A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix. *Econometrica*, 55(3), 703–708. (Basis for HAC SE implementation.)

U.S. Energy Information Administration (2026). Short-Term Energy Outlook — Heating Degree Days by Census Division. STEO Table Browser, Series ZWHD_NEC. Retrieved January 2026.

Federal Reserve Bank of St. Louis (2026). APU000072511: Average Price: Heating Oil, No. 2 per Gallon. FRED Economic Data. Retrieved January 2026.

Federal Reserve Bank of St. Louis (2026). CPIAUCSL: Consumer Price Index for All Urban Consumers. FRED Economic Data. Retrieved January 2026.

---

## AI Audit Appendix Summary

Full AI audit documentation is maintained in `AI_AUDIT_APPENDIX.md` in the project repository. The appendix covers all 10 documented uses of Claude (claude-sonnet-4-6 via Claude Code CLI) across M1 (Uses 1–3), M2 (Uses 4–6), M3 (Uses 7–10), and M4 (this memo). For each use, we record: the exact prompt, the AI output received, how we verified the output, and a critique of where the AI was helpful, where it required correction, and what the team added independently.

**Key examples of AI correction and independent human contribution:**
- *M1*: AI omitted `units='standard'` in the NOAA API call; we caught this by reading primary NOAA documentation and knowing that U.S. HDD is Fahrenheit-based. Without the correction, all HDD values would have been ~30% lower.
- *M2*: AI suggested a 12-month rolling correlation window; we changed it to 24 months after recognizing that structural shifts (shale era transition) operate on multi-year timescales.
- *M3*: AI draft used `sm.add_constant()` in a train/test context where Post2014=1 for all test observations; the bug produced no visible error but would have generated incorrect predictions. Caught only by end-to-end testing.
- *M3 (Bonus)*: AI recommended a Difference-in-Differences placebo test for the structural break; we rejected this because our Post2014 dummy is a level-shift control, not a treatment effect estimator — conflating DiD logic with a regime dummy would have been an econometric error.

All AI outputs were treated as first drafts. Specification decisions, diagnostic interpretations, and economic conclusions were verified by the team against course materials and primary literature before inclusion in any submission. **We take full ownership of all work in this memo and the associated code repository.**

---

---

# Individual Addendums

---

## Individual Addendum: Matthew Talburt

**Course:** QM 2023 — Statistics II: Data Analytics
**Team:** 4th Row Team
**Submission Date:** May 1, 2026

### Specific Contributions

| Milestone | Task | Hours |
|-----------|------|-------|
| M1 | FRED API integration (`fetch_fred_series`): pulled APU000072511 and CPIAUCSL, verified against FRED website for Jan 2020 spot-check | 6 hrs |
| M1 | NOAA API pagination fix: split 2000–2025 into three decade-length requests; added `units='standard'` after reading NOAA CDO documentation | 5 hrs |
| M1 | Pipeline integration and `load_api_keys()` function; retry/error handling around HTTP 429 responses | 3 hrs |
| M2 | Geographic mismatch identification: read FRED APU000072511 series documentation and identified that Boston Logan single station does not match the national average price series scope | 4 hrs |
| M3 | EIA NEC_HDD data pull (`enrich_panel.py`): sourced STEO ZWHD_NEC and ZWHDPUS series; verified population-weighting methodology against EIA documentation | 5 hrs |
| M4 | Scenario analysis table (Table 3); probability-weight calculations; investment recommendation drafting | 4 hrs |
| **Total** | | **~27 hrs** |

### Defended Methodological Decision

**Decision:** Replacing the Boston Logan NOAA single weather station (GHCND:USW00014739) with the EIA New England Census Division population-weighted HDD series (STEO ZWHD_NEC) as the primary HDD measure.

This decision came from reading the FRED series documentation for APU000072511, which describes it as a *national city average* heating oil price — not a Boston or New England price. Using a single Boston weather station to explain a national price series is a geographic mismatch: we would be testing whether one city's coldness affects the average price across dozens of cities. The EIA NEC series is population-weighted across MA, ME, NH, VT, CT, and RI — the six states that account for approximately 75% of U.S. heating oil consumption — which directly aligns with the scope of the price series we are trying to explain.

The M3 Geographic Robustness Check (Robustness 5) validates this choice: all three HDD measures — Boston Logan, NEC population-weighted, and national U.S. — yield statistically indistinguishable null results (p = 0.624–0.700). This rules out the geographic mismatch as an explanation for the null and focuses attention on the economic mechanism: globalization of crude oil supply has severed the weather-price link regardless of how weather is measured.

### Key Limitation

The FRED price series (APU000072511) is a national city average, not a New England regional price. New England historically carries a geographic premium due to limited pipeline infrastructure — the region is served primarily by marine terminals and the Buckeye Pipeline rather than the Colonial Pipeline that supplies the South and Mid-Atlantic. If we had access to the EIA New England-specific retail heating oil price series (EIA-182 survey), we might observe a small but detectable relationship between NEC_HDD and the *regional* price premium, even after the global crude channel is accounted for. Our null result is therefore strictly a statement about *national average prices*: it does not preclude weather having a small localized effect on the New England retail price spread above the national benchmark. Future work could test this by differencing the New England price from the national average and regressing the spread on NEC_HDD.

### AI Audit Notes for My Work

Used Claude Code to draft the NOAA API pagination logic (Use 2) and the `enrich_panel.py` EIA data pull. In both cases, the AI required domain-knowledge corrections: `units='standard'` for NOAA (Fahrenheit vs. Celsius HDD), and verification of EIA STEO series IDs by cross-checking the EIA website against the STEO documentation. The geographic mismatch identification (the most consequential contribution to the project's validity) required reading primary documentation — the AI had no way to flag this without being told which FRED series we were using.

---

## Individual Addendum: Joshua Keoshkarian

**Course:** QM 2023 — Statistics II: Data Analytics
**Team:** 4th Row Team
**Submission Date:** May 1, 2026

### Specific Contributions

| Milestone | Task | Hours |
|-----------|------|-------|
| M2 | `capstone_eda.ipynb` — all 8 required visualizations (correlation heatmap, time series, dual-axis, lagged correlation, rolling correlation, subsample, scatter/decomposition, seasonal decomposition) | 8 hrs |
| M2 | `config_paths.py` module: relative path configuration tested from both project root and `code/` subdirectory | 2 hrs |
| M2 | Economic captions for all 8 plots; updated captions after running notebook to reflect actual near-zero correlation (AI had assumed positive HDD-price correlation) | 3 hrs |
| M2 | M2_EDA_summary.md: five key findings, three M3 hypotheses, data quality table | 3 hrs |
| M3 | Rolling correlation analysis for M3 caveats section; confirmed non-stationarity of HDD-price relationship across all subperiods | 2 hrs |
| M4 | Results section, Figure descriptions, robustness summary table | 4 hrs |
| **Total** | | **~22 hrs** |

### Defended Methodological Decision

**Decision:** Using a 24-month rolling window for the rolling correlation analysis (Plot 5 in M2) instead of the AI-suggested 12-month window.

The AI initially generated the rolling correlation with a 12-month window, which is the typical default for monthly seasonal data. I changed this to 24 months after thinking through what we are actually trying to detect: the research question asks whether *globalization* (a multi-year structural shift) has severed the HDD-price link. A 12-month window would capture year-to-year variation — including random annual fluctuations — and make the rolling correlation appear more volatile than the underlying structural relationship. A 24-month window smooths out single-year noise and highlights genuine regime changes: the shale era transition (2014–2016), the COVID demand collapse (2020), and the post-war normalization (2022–2025). Under the 24-month window, we can clearly see that the HDD-price correlation never sustains a positive value for more than a few consecutive months across the entire 25-year sample — a much stronger statement than the 12-month version would produce.

This choice directly strengthened the research narrative: rather than showing a noisy, occasionally positive relationship, the 24-month rolling correlation demonstrates that the null result is a *structural feature* of the market, not a statistical artifact of a particular sample period.

### Key Limitation

Monthly frequency may obscure short-lived polar vortex effects. Heating oil demand during a polar vortex event is heavily concentrated in the coldest 72–96 hours, when temperatures fall far below seasonal averages. Monthly HDD aggregates the entire month — including warm shoulder days before and after the cold snap — smoothing out the intensity signal. At the weekly or even daily frequency, a brief extreme cold event might produce a detectable short-lived price spike (a 3–5 day "weather window" that disappears by month-end as logistics respond). Our finding that monthly HDD has no effect does not rule out this sub-monthly price response. Testing it would require weekly EIA retail price data and high-frequency weather station data — a data collection effort beyond the scope of this project, but a meaningful extension for a commodity risk management context where intra-month hedging is relevant.

### AI Audit Notes for My Work

Used Claude Code to scaffold the EDA notebook structure (Use 5 in AI_AUDIT_APPENDIX). The AI's initial axis labeling used the raw CPI-ratio version of real price (values like "0.018"), not the 2020-dollar-rescaled version. I caught this because the axis values were uninterpretable and fixed it by requesting the rescaling. The AI also assumed in several captions that HDD and price "should be positively correlated" — I corrected all eight captions after running the notebook and observing the actual near-zero correlation. These corrections required understanding what the data actually showed, not what economic intuition naively predicts.

---

## Individual Addendum: Jeret Stone

**Course:** QM 2023 — Statistics II: Data Analytics
**Team:** 4th Row Team
**Submission Date:** May 1, 2026

### Specific Contributions

| Milestone | Task | Hours |
|-----------|------|-------|
| M3 | `capstone_models.py` — Model A (Dynamic OLS, three specifications: standard SE, HC3, interaction) | 7 hrs |
| M3 | ADF stationarity test, Breusch-Pagan test, VIF calculation, Durbin-Watson statistic | 3 hrs |
| M3 | Robustness Checks 1–4 (SE comparison, lag structure, crisis exclusion, subsample split) | 4 hrs |
| M3 | Model B (OLS vs Random Forest, 80/20 chronological split, feature importance, comparison plot) | 4 hrs |
| M3 | Caught and fixed `sm.add_constant` bug in Model B test-set prediction (Post2014=1 for all test obs) | 2 hrs |
| M3 | Bootstrap SE (1,000 replications, residual bootstrap) and Newey-West HAC SE bonus implementation | 3 hrs |
| M4 | Methodology section (2.3 model specifications, equation formatting); Table 1 and Table 2 | 3 hrs |
| **Total** | | **~26 hrs** |

### Defended Methodological Decision

**Decision:** Using Dynamic OLS (AR(1) lagged dependent variable) instead of PanelOLS with entity fixed effects.

The M3 rubric specifies "Fixed Effects regression," but our dataset is a single time series with no entity dimension — there is literally only one entity (the U.S. national heating oil market). PanelOLS with `entity_effects=True` in `linearmodels` sweeps out cross-sectional means by demeaning each entity. With a single entity, every observation is the entity — demeaning would subtract the grand mean from every observation and produce results identical to OLS on demeaned data, adding no information. More critically, `cov_type='clustered'` in `linearmodels` (which clusters SE at the entity level) requires multiple entities to be valid — a requirement we cannot satisfy.

Dynamic OLS is the correct single-entity analogue: it controls for time-invariant entity characteristics through the lagged dependent variable (which captures all persistent entity-specific pricing dynamics, including management of inventory, geographic infrastructure, and historical price levels) and uses HC3/HAC standard errors for heteroskedasticity and serial correlation corrections. This choice is validated by Hamilton (1994, *Time Series Analysis*, Ch. 17), who shows that the AR(1) lagged dependent variable approach is standard for persistent single-entity commodity time series. We documented this reasoning explicitly in the model script comments and the AI Audit Appendix so the adaptation from the rubric template is transparent to the grader.

### Key Limitation

The ADF test (p = 0.047) barely rejects the unit root at 5%, placing the real price series in a gray zone between stationarity and near-integrated behavior. If the series were truly I(1) (integrated of order 1), regressing it on another near-I(1) variable (the lagged price) would produce spurious results despite high R². The Dynamic OLS approach with an AR(1) term is robust to both I(0) and near-I(1) specifications because it models price growth rather than levels — the coefficient on the lagged dependent variable captures whatever degree of persistence is present, whether finite or unit-root. However, a proper I(1) treatment (cointegration testing, error-correction model) would be warranted if we believed the series was definitively non-stationary. The Johansen cointegration test for a potential cointegrating relationship between heating oil prices and WTI crude would be a principled extension.

### AI Audit Notes for My Work

The most important AI error I caught was the `sm.add_constant` bug in Model B (Use 7 in AI_AUDIT_APPENDIX). The AI's test-set prediction code used `sm.add_constant(X_test)` — which silently skips adding a constant column when any existing column is constant. Because Post2014 = 1 for every observation in the 2020–2025 test period, `sm.add_constant` treated the constant as already present and added nothing. The model then predicted without an intercept, producing systematically biased test-set forecasts with no visible error message. I caught this by running the code end-to-end, examining the out-of-sample predictions, and noticing that the OLS test R² was implausibly low on the first run. The fix — manually inserting a `const` column before fitting — required understanding what `sm.add_constant` actually does. This is the clearest example in the project where running the code was non-negotiable; the AI's output looked syntactically correct but was functionally wrong.

---

## Individual Addendum: Cooper Worsham

**Course:** QM 2023 — Statistics II: Data Analytics
**Team:** 4th Row Team
**Submission Date:** May 1, 2026

### Specific Contributions

| Milestone | Task | Hours |
|-----------|------|-------|
| M1 | AI_AUDIT.md documentation — all three M1 uses; row-count assertion (`assert len(panel) == 311`) added to pipeline for reproducibility | 3 hrs |
| M2 | M2_EDA_summary.md — geographic mismatch flag and recommendation to switch HDD source from NOAA station to EIA NEC series | 2 hrs |
| M3 | Robustness Check 5 (geographic HDD comparison: NEC, national, Boston) — wrote specification, ran results, confirmed null holds across all three | 3 hrs |
| M3 | Diagnostic interpretation write-up for M3_interpretation.md — all five diagnostic sections (Breusch-Pagan, VIF, residuals, Durbin-Watson, bootstrap) | 4 hrs |
| M3 | Rejected AI-suggested DiD placebo test; documented reasoning in M3_interpretation.md Caveats section | 1 hr |
| M3 | AI_AUDIT_APPENDIX.md — all nine M3 uses; updated M2/M3 summary tables | 3 hrs |
| M4 | Team memo drafting — Executive Summary, Recommendations, Caveats, References, AI Audit Appendix summary | 6 hrs |
| M4 | Individual addendum coordination; Use 10 AI audit entry (Newey-West HAC) | 2 hrs |
| **Total** | | **~24 hrs** |

### Defended Methodological Decision

**Decision:** Rejecting the AI's suggestion of a Difference-in-Differences (DiD) placebo test for the Post-2014 structural break, and retaining the Post2014 dummy as a level-shift control variable instead.

During M3, the AI suggested validating the 2014 structural break using a DiD-style placebo test — randomly assigning the break year to an earlier period (e.g., 2009 or 2011) and confirming that the "effect" disappears. This is standard practice when the Post2014 indicator is being used as a *treatment variable* in a causal DiD design. However, our Post2014 dummy is not a treatment variable — it is a level-shift control capturing the permanent downward price adjustment caused by the 2014 shale supply glut. We are not trying to estimate the *causal effect* of the shale revolution on heating oil prices; we are controlling for the known structural price decline so that the HDD coefficient is estimated on a common price scale across both eras.

Applying DiD placebo logic to a regime control variable would conflate two econometrically distinct designs. A placebo test for a level-shift control does not make the HDD coefficient more credible — it would only test whether our regime dummy is correctly dated, which we verified independently through EIA crude production data (U.S. output crossed 9 mb/d in Q4 2014; Saudi Arabia declined to cut OPEC quotas in November 2014). Knowing when to reject an AI suggestion required understanding this distinction. I documented the rejection explicitly in M3_interpretation.md to demonstrate that we engaged critically with the AI's output rather than accepting it uncritically.

### Key Limitation

Our study covers a single commodity (heating oil, FRED APU000072511) in a single market (U.S. national average). The finding that weather does not move U.S. national heating oil prices may not generalize to:

- **Other heating fuels:** Natural gas and electricity have more localized pricing dynamics because pipelines are capacity-constrained during polar vortex events in ways that ocean-freight distillate markets are not.
- **Other geographies:** European heating oil markets may show stronger weather sensitivity because European crude supply is more constrained and less elastic than the U.S. shale-backed system.
- **Pre-2000 periods:** The FRED price series extends to 1978. Our sample begins in 2000 due to HDD data availability. The pre-shale, pre-globalization era (1978–1990) may have shown a stronger weather-price link when the U.S. was more dependent on domestic or regional supply chains.

The investment recommendation is therefore strongest for U.S. heating oil specifically, in the current post-shale era. Firms with significant European heating fuel exposure, natural gas distribution, or utility operations in capacity-constrained markets should not apply the null result universally without first testing the same specification on their specific market data.

### AI Audit Notes for My Work

The geographic mismatch flag — identifying that our original NOAA single-station HDD was incompatible with the national scope of the FRED price series — came from reading primary documentation, not from AI prompting. When I wrote up the M2 summary document (Use 6 in AI_AUDIT_APPENDIX), the AI produced a thorough structural framework but did not flag the mismatch because we had not told it which FRED series we were using or what its geographic definition was. I caught it by separately reading the FRED series description, which explicitly states "U.S. City Average Price." The consequence of not catching this would have been a fundamentally misspecified research question: measuring whether Boston coldness affects the average price across Boston, New York, Philadelphia, Chicago, and Los Angeles. The 5th robustness check — confirming the null holds under all three HDD measures — validates that the correction mattered but did not change the substantive finding. Knowing what to look for in primary documentation is a skill that no amount of AI prompting replaces.
