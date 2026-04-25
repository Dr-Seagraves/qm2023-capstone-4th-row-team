# AI Audit Appendix — Milestones 1, 2 & 3

**QM 2023 Capstone | 4th Row Team | Spring 2026**
**Research Question:** Has the globalized energy supply chain severed the link between severe U.S. winters and domestic heating oil prices?

---

## Purpose

This appendix documents all uses of AI tools (Claude via Claude Code CLI) across all three milestones of the capstone project. For each use we record: the prompt given to the AI, the output received, how we verified that output, and our critical assessment of where the AI was helpful, where it required correction, and what the team added independently.

All AI outputs were treated as first drafts. Specification decisions, diagnostic interpretations, and economic conclusions were verified by the team against course materials, textbook references, and the M2 EDA findings before inclusion in any submission.

---

# Milestone 1 — Data Pipeline

## Use 1 — FRED API Data Fetch

**Tool:** Claude (claude-sonnet-4-6 via Claude Code CLI)

**Prompt given:**
> "I need to pull heating oil prices and CPI from the FRED API using Python. The series IDs are APU000072511 for heating oil and CPIAUCSL for CPI. I have an API key already stored in a .secrets file. How do I fetch both series and merge them into one dataframe?"

**Output received:**
A Python function `fetch_fred_series(series_id)` that calls the FRED observations endpoint, filters out missing-value placeholders (`'.'`), converts values to numeric, and returns a tidy DataFrame. The merge step joined on `date` with `suffixes=('_Nominal', '_CPI')` and derived the real price ratio.

**Verification:**
- Ran the script and confirmed the API returned 565 rows for the price series (January 1978 onward) and 793 rows for CPI (January 1947 onward) — only observations from 2000 onward are relevant.
- Verified that `df['value'] != '.'` correctly removes FRED's placeholder for missing monthly observations.
- Confirmed `pd.to_numeric(df['value'], errors='coerce')` doesn't silently drop valid rows by checking the row count before and after.
- Spot-checked the January 2020 heating oil price against the FRED website directly: FRED shows $2.897/gallon, pipeline output matches.
- Verified the real price formula: `Real_Heating_Oil_Price = Heating_Oil_Price / CPI` — this is a dimensionless ratio, intentionally left unnormalized at this stage (2020-dollar rescaling applied in M3).

**Critique:**
The AI's fetch function works correctly. One issue: it did not include retry logic for rate-limit responses (HTTP 429). We added a `try/except requests.HTTPError` block around the API call ourselves after noticing that repeated test runs occasionally failed silently. The AI correctly used `response.raise_for_status()` so errors are at least visible, but production code should retry. For a capstone project this is acceptable.

---

## Use 2 — NOAA API Pagination Fix

**Tool:** Claude (claude-sonnet-4-6 via Claude Code CLI)

**Prompt given:**
> "My NOAA API call for Boston Logan heating degree days is only returning 1000 rows even though I need 25 years of monthly data. The API limit is 1000 results per request. How do I split the request into date ranges to get all the data? Station ID is GHCND:USW00014739, dataset GSOM, datatype HTDD."

**Output received:**
A `date_ranges` list splitting the 2000–2025 window into three decade-length chunks, each fetched separately and concatenated into a single DataFrame. The station ID, dataset ID, and datatype were passed through correctly.

**Verification:**
- Confirmed that three separate requests (2000–2009, 2010–2019, 2020–2025) each return fewer than 1000 rows (120, 120, and ~72 respectively), so none hit the pagination limit.
- Verified total row count: 312 rows in `noaa_clean.csv` — consistent with 25+ years of monthly data minus 1 known gap (October 2025, noted in the data dictionary).
- Cross-checked January 2010 HDD value (Boston Logan, GSOM HTDD) against the NOAA CDO web interface: NOAA reports 1,002 HDD for that month; pipeline output matches.
- Confirmed `units='standard'` is correct for Fahrenheit-based HDD (U.S. standard); `units='metric'` would return Celsius-based values.

**Critique:**
The AI did not initially include the `units='standard'` parameter. We caught this by checking the NOAA CDO documentation and noticing that omitting `units` defaults to metric (Celsius). Boston's coldest months would show values roughly 30% lower under Celsius HDD, which would have been inconsistent with EIA benchmarks. We added the `units='standard'` parameter independently. This is an example where domain knowledge — knowing that U.S. heating degree days are conventionally Fahrenheit-based — was required to catch the AI's omission.

---

## Use 3 — Merge Strategy and Missing Month Handling

**Tool:** Claude (claude-sonnet-4-6 via Claude Code CLI)

**Prompt given:**
> "Should I use an inner join or outer join when merging the FRED price data with the NOAA heating degree day data? FRED goes back to 1978, NOAA I only have from 2000. Also NOAA is missing October 2025. What happens to that row?"

**Output received:**
Recommendation to use `pd.merge(..., how='outer')` followed by `dropna(subset=['Heating_Degree_Days', 'Real_Heating_Oil_Price'])`. This keeps the merge transparent (outer join preserves all rows so you can see what gets dropped) while ensuring the final dataset has no missing values in the analysis columns. The AI also noted that the October 2025 missing NOAA row would produce a NaN for `Heating_Degree_Days` and be removed by `dropna`, resulting in 311 (not 312) complete rows.

**Verification:**
- Ran the merge and confirmed `panel.shape` is `(311, 5)` — the outer join correctly drops the pre-2000 FRED rows and the missing October 2025 NOAA row.
- Confirmed `panel.isna().sum()` is zero across all columns in the final output.
- Verified that using `how='inner'` would give the same 311-row result given these two specific datasets, but `how='outer'` with `dropna` is more transparent because it makes the dropped rows inspectable before the drop step.
- Noted the October 2025 gap in `data/final/DATA_DICTIONARY.md` as a known limitation.

**Critique:**
The AI's merge recommendation is correct. We independently decided to add a row-count assertion (`assert len(panel) == 311`) after the merge, which is not something the AI suggested but is good defensive practice for reproducibility. If a future data pull returns an extra month (e.g., if NOAA backfills October 2025), the assertion will flag it rather than silently changing the sample size.

---

## M1 Summary of AI Use

| # | Task | Tool | Time saved | Human additions |
|---|------|------|-----------|-----------------|
| 1 | FRED API fetch function | Claude Code | ~45 min | Added retry/error handling; verified against FRED website |
| 2 | NOAA pagination fix | Claude Code | ~30 min | Added `units='standard'`; verified against CDO web interface |
| 3 | Merge strategy | Claude Code | ~20 min | Added row-count assertion; documented October 2025 gap |

**Total AI-assisted code for M1:** ~60 lines of the 101-line `code/main_panel.py`.
**Lines written or modified independently:** ~41 lines (error handling, path setup, the `load_api_keys()` function, output logging, the `assert` statement).

---

# Milestone 2 — Exploratory Data Analysis

## Use 4 — `config_paths.py` Module

**Tool:** Claude (claude-sonnet-4-6 via Claude Code CLI)

**Prompt given:**
> "M1 feedback said we had hardcoded paths in the pipeline script. I need a config_paths.py that defines the project root and all subdirectory paths so nothing is hardcoded. It should work whether I run the script from the project root or from inside the code/ folder. Directories should be created automatically on import."

**Output received:**
A module using `pathlib.Path(__file__).resolve().parent` to anchor all paths relative to the file's location, with a loop calling `_dir.mkdir(parents=True, exist_ok=True)` for each output directory on import.

**Verification:**
- Tested `from config_paths import FIGURES_DIR` from both the project root and from within `code/` — resolved correctly in both cases.
- Verified `FIGURES_DIR` points to `results/figures/` as required by the assignment rubric (not a `figures/` folder at the root).
- Confirmed `exist_ok=True` means the import is idempotent — running it multiple times doesn't raise errors.
- Deleted `results/figures/` manually and confirmed the import recreated it.

**Critique:**
The AI's design is clean and robust. We added explicit exports (`FINAL_DIR`, `TABLES_DIR`, `FIGURES_DIR`) to the module ourselves after reviewing which directories were actually needed downstream, since the AI generated a slightly more generic version. The `Path(__file__)` pattern is correct and preferable to `os.getcwd()`, which would break if the working directory at runtime differs from the project root.

---

## Use 5 — EDA Notebook Structure

**Tool:** Claude (claude-sonnet-4-6 via Claude Code CLI)

**Prompt given:**
> "I need to build the M2 capstone_eda.ipynb. Our dataset is a single monthly time series — Real Heating Oil Price vs Heating Degree Days, 2000–2025, no panel structure. The rubric requires 8 plots: correlation heatmap, time series, dual-axis, lagged correlation, rolling correlation, time period subsample, scatter plots, and decomposition. Each plot needs an economic caption and all need to be saved to FIGURES_DIR at 300 DPI. Can you help me set up the notebook structure and the first few cells?"

**Output received:**
A complete Jupyter notebook outline with 8 visualization cells, feature engineering (real price in 2020 dollars, lagged HDD variables, period classification), economic narrative cells, and summary statistics. Each `plt.savefig()` call used `FIGURES_DIR / 'plotN_...'` from `config_paths`.

**Verification:**
- Checked all column name references against `data/final/final.csv` header: `YearMonth`, `Heating_Oil_Price`, `CPI`, `Real_Heating_Oil_Price`, `Heating_Degree_Days` — all matched.
- Verified `pd.to_datetime(df['YearMonth'], format='%Y-%m')` correctly parses the "YYYY-MM" string format in the CSV.
- Confirmed `seasonal_decompose(ts, model='additive', period=12)` is appropriate for a monthly series — period=12 matches the annual heating cycle.
- Ran all 8 cells end-to-end, confirmed all PNG files were saved to `results/figures/`.
- Reviewed the rolling correlation window choice: the AI used 12 months initially, we changed it to 24 months independently because a 24-month window is better suited to detecting multi-year structural shifts (the shale era transition takes several years, not several months). This directly improved the research narrative.

**Critique:**
The AI used `Real_Heating_Oil_Price` (the raw CPI-ratio column from the CSV) directly for axis labels, which produces uninterpretable axis values like "0.018" instead of "$2.50/gallon." We caught this and requested a rescaled 2020-dollar version, which was incorporated. The economic captions were plausible but contained assumed correlation signs ("HDD and price should be positively correlated") that needed updating after running the notebook — which showed near-zero correlation. We updated all captions to reflect the actual findings.

---

## Use 6 — M2 EDA Summary Document

**Tool:** Claude (claude-sonnet-4-6 via Claude Code CLI)

**Prompt given:**
> "Write an M2_EDA_summary.md based on what we found in the notebook. Key results: HDD has basically zero correlation with real price at every lag from 0 to 12 months, correlation is like -0.005 to +0.011. WTI crude has r = 0.946. AR(1) autocorrelation is 0.979. We see a potential structural break around 2014 (shale). The three M3 hypotheses should be: (1) HDD has no effect on price after controlling for AR(1), (2) the HDD effect diminished post-2014 shale era, (3) a heating season dummy captures remaining seasonal effect."

**Output received:**
A structured markdown document with 5 key findings, 3 M3 model hypotheses (each with expected sign, mechanism, and test strategy), and a data quality table with flags and mitigations.

**Verification:**
- Verified all correlation values cited match the notebook output: r(HDD, Real_Price) ranges from -0.005 to +0.011 across lags 0–12 — confirmed against Plot 4.
- Verified the structural break narrative against Plot 5 (rolling correlation): the 24-month rolling correlation confirms the relationship was near-zero throughout the entire sample, not just post-2014.
- The note about geographic mismatch (Boston Logan single station vs. national average price) was added by us — the AI did not flag this. We caught it by reading the FRED APU000072511 documentation, which describes the series as a national city average, not Boston-specific. This was a substantive limitation that shaped the entire M3 design.
- Checked that the model specifications in the hypotheses section are syntactically correct for time-series OLS.

**Critique:**
The AI's coefficient magnitude estimates in Hypothesis 1 ("likely in the range of $0.001–0.003/gal per HDD") were uninformed placeholders. We replaced these with actual M3 regression results after running the models. The geographic mismatch limitation — our most important data quality flag — required us to read primary source documentation rather than relying on AI. The AI produced a thorough structural framework; we provided the domain-specific content.

---

## M2 Summary of AI Use

| # | Task | Tool | Time saved | Human additions |
|---|------|------|-----------|-----------------|
| 4 | config_paths.py | Claude Code | ~20 min | Added specific exports, tested from subdirectory |
| 5 | capstone_eda.ipynb | Claude Code | ~3 hours | Changed rolling window to 24 months; fixed axis units; updated captions to match actual results |
| 6 | M2_EDA_summary.md | Claude Code | ~1 hour | Added geographic-mismatch flag; corrected coefficient magnitude estimates; verified all correlation values |

**Total AI-assisted content for M2:** ~500 lines across notebook and documentation.
**Lines written or modified independently:** ~90 lines plus all final caption text and the geographic mismatch analysis.

---

# Milestone 3 — Econometric Models

## Use 7 — Econometric Specification Design

**Tool:** Claude (claude-sonnet-4-6 via Claude Code CLI)

**Prompt given:**
> "I need to build capstone_models.py for M3. Our data is a single time series — 311 monthly obs, not a panel. The rubric says to use a Fixed Effects model but we only have one entity so PanelOLS doesn't make sense. What's the right model for us? We found in M2 that AR(1) autocorrelation is 0.979 and HDD has basically no correlation with price at any lag. Should we include WTI in the model?"

**Output received:**
Recommendation for Dynamic OLS (AR(1) lagged dependent variable) as the single-entity equivalent of Fixed Effects, with explicit justification that PanelOLS entity fixed effects require multiple entities to be identified. Three model specifications: standard SE (baseline), HC3 robust SE (preferred given heteroskedasticity detected in M2), and an HDD×Post2014 interaction term to test the structural break hypothesis. Also recommended keeping WTI out of Model A to isolate the HDD-to-price channel, and including it only in Model B (ML comparison) to show what happens to HDD's importance when WTI is available as a competing predictor.

**Verification of specification decisions:**

1. **Why Dynamic OLS instead of PanelOLS:** We verified against Hamilton (1994, *Time Series Analysis*, Ch. 17): including a lagged dependent variable in OLS is the standard approach for single-entity time series with persistent autocorrelation. PanelOLS with `entity_effects=True` sweeps out cross-sectional means — with one entity, there is no cross-sectional variation to sweep and the demeaning step is a no-op. The rubric was written for REIT panel data; Dynamic OLS is the correct adaptation for a time series.

2. **Why HDD at lag 1:** M2 Plot 4 showed near-zero bivariate correlation at all lags 0–12. Lag 1 is the economically motivated default (a cold month affects next month's prices through inventory drawdown and forward purchasing contracts). The lag-structure robustness check confirms this: all lags 0–3 yield p > 0.60.

3. **Why HC3 and not clustered SE:** Clustered SE corrects for within-group serial correlation across multiple entities — for a single time series, the correct correction for heteroskedasticity is a heteroskedasticity-consistent SE estimator (HC3). We confirmed heteroskedasticity was present via Breusch-Pagan in M2 visual inspection and verified formally in M3 (LM = 26.50, p < 0.0001).

4. **Why exclude WTI from Model A:** The goal of Model A is to estimate the direct HDD-to-price channel. Including WTI would partially absorb the global commodity cycle, which is exactly the mechanism we are testing against. The bivariate correlation between WTI and NEC_HDD is r ≈ 0.01, so omitted variable bias from excluding WTI is minimal. WTI's role is shown in Model B (RF feature importance: WTI = 14.3%).

**Critique:**
The AI's initial draft used `sm.add_constant(X_train)` for the OLS component of Model B. During testing this caused a `ValueError: shapes not aligned` because the test set covers 2020–2025 — a period where `Post2014=1` for every observation, making the column constant and causing `sm.add_constant` to silently skip adding an intercept. The fix (manually inserting a `const` column before fitting) was identified during end-to-end testing and applied independently. This is the most important example of a bug that would not have been caught without actually running the code — the script would have produced incorrect predictions silently.

---

## Use 8 — Diagnostic Interpretation

**Tool:** Claude (claude-sonnet-4-6 via Claude Code CLI)

**Prompt given:**
> "Here are our M3 diagnostic results. Can you help write the diagnostics section for M3_interpretation.md? Breusch-Pagan: LM = 26.50, p < 0.0001. VIF: all predictors < 1.32. Residual plot: scatter is tighter at low fitted values and fans out above $4/gal, corresponding to 2008 and 2022. Q-Q plot: normal in the middle but heavy tails, kurtosis around 8. ADF test on the price level: p = 0.047, just barely rejects the unit root at 5%."

**Output received:**
Interpretation of each diagnostic with: statistical result, implication for coefficient validity, fix applied, and confirmation that the fix does not change the substantive conclusion. The ADF borderline result was characterized as consistent with a near-I(1) process and the Dynamic OLS AR(1) specification was described as robust to this ambiguity.

**Verification:**
- ADF borderline: We verified against the critical values printed by statsmodels: 5% critical value = -2.871; our ADF statistic = -2.884, just past the threshold. The borderline characterization is accurate. The AR(1) lagged dependent variable absorbs price persistence whether the series is I(0) or near-I(1), so the specification is robust either way.
- Kurtosis ≈ 8.2: We confirmed the source is the 2008 GFC and 2022 Russia-Ukraine war price spikes by computing the residual series and identifying outlier observations. OLS is consistent under non-normal errors by the CLT — kurtosis affects finite-sample confidence interval coverage but not point estimates.
- HC3 vs HC1/HC2: We verified the AI's preference for HC3 against Long & Ervin (2000, "Using Heteroscedasticity Consistent Standard Errors in the Linear Regression Model") — HC3 is the recommended estimator when high-leverage observations are present, which our crisis-period spikes are. The paper notes HC3 can be slightly conservative for very small n, which is not a concern at n = 310.

**Critique:**
The diagnostic write-up is accurate and appropriately hedged. The AI correctly noted that leptokurtosis does not bias OLS estimates — this is a common misconception among students who conflate the normality assumption (needed for exact finite-sample inference) with the Gauss-Markov conditions (which only require E[ε|X] = 0 and homoskedasticity for BLUE). One thing the AI initially understated: the heavy tails are economically interpretable, not just a nuisance — they reflect genuine tail risk from geopolitical shocks that any realistic model of heating oil prices must acknowledge. We added language in the Caveats section to make this explicit.

---

## Use 9 — Robustness Check Design

**Tool:** Claude (claude-sonnet-4-6 via Claude Code CLI)

**Prompt given:**
> "We need at least 3 robustness checks for our dynamic OLS. The main things we're worried about: did we just get lucky with lag 1 for HDD, could the 2008 crash or COVID be making HDD look insignificant because they dominate the variance, and does the Post2014 structural break argument actually hold up. What are the right checks to run?"

**Output received:**
Four robustness checks:
1. Standard SE vs HC3 (already in Models 1 and 2 — compare coefficient stability across SE specification)
2. HDD at lags 0, 1, 2, 3 — all coefficients and p-values
3. Re-estimate excluding 2008–09 and 2020 crisis years
4. Pre-2014 vs post-2014 subsample split

We extended this to a fifth check (geographic HDD comparison) independently.

**Verification:**
- Lag structure: All four lags are economically defensible — lag 0 = contemporaneous demand, lag 1 = next-month delivery pricing, lags 2–3 = forward contract pricing. All lags yield p > 0.60, confirming the null is not lag-specific.
- Crisis exclusion: We excluded 2008–09 (GFC) and 2020 (COVID) but not 2022 (Ukraine war), because the research question is about the globalization/shale structural change rather than geopolitical shocks. The 2022 shock is a supply shock driven by the Russia-Ukraine war — excluding it would obscure the channel we're studying. This judgment call was made independently.
- Subsample split at 2014: The AI correctly used the shale threshold from M2. We independently confirmed that U.S. crude production crossed 9 mb/d in Q4 2014 and that Saudi Arabia declined to cut OPEC quotas in November 2014 — both supply-side events justifying the 2014 regime break.
- Geographic HDD check (Robustness 5, added by team): The geographic mismatch concern from M1 motivated a fifth check comparing NEC_HDD (EIA, New England Census Division, population-weighted), US_HDD (EIA national), and Boston_HDD (NOAA single station). All three yield statistically indistinguishable null results (p = 0.624–0.700), ruling out measurement error in HDD as an explanation. This check was not in the AI's output — it came directly from the geographic mismatch concern we identified when building the dataset.

**Critique:**
The AI suggested adding a placebo test — running a DiD regression as if the Post2014 break had occurred in an earlier period. We did not implement this because we are not running a Difference-in-Differences model. Our Post2014 dummy is a level-shift control capturing the structural price decline after the 2014 shale glut, not a causal treatment effect. Applying DiD placebo logic to a regime dummy conflates two distinct econometric designs. We noted this in M3_interpretation.md (Caveats section). Knowing when to reject an AI suggestion required understanding the difference between a DiD design and a structural break control.

---

## Use 10 — Newey-West (HAC) Standard Errors (Bonus)

**Tool:** Claude (claude-sonnet-4-6 via Claude Code CLI)

**Prompt given:**
> "Our M3 diagnostic shows DW = 1.27 — mild residual serial correlation. The summary already notes 'Newey-West SE would be a further robustness check.' Can you implement Newey-West HAC SE as a bonus and explain the bandwidth choice? Use the same Model A specification."

**Output received:**
Section 5.6 of `capstone_models.py`: `sm.OLS(y_A, X_A).fit(cov_type='HAC', cov_kwds={'maxlags': 12})`. A comparison table prints Standard, HC3, and HAC results side-by-side for the HDD_lag1 coefficient, with a note that positive residual autocorrelation (DW < 2) causes HAC SE > HC3 SE, yielding a p-value that exceeds 0.689 and further confirms the null.

**Verification:**
- Confirmed `cov_type='HAC'` in statsmodels implements the Newey-West (1987) heteroskedasticity- and autocorrelation-consistent estimator — verified against statsmodels documentation.
- Bandwidth selection: the Newey-West (1994) data-driven rule gives ≈ 6 lags for n = 310; we used 12 to conservatively cover the full annual heating cycle (October–March), at the cost of slightly wider SE. The wider SE makes the null result more, not less, conservative.
- Verified that HAC SE > HC3 SE is the expected direction with positive residual autocorrelation: positive serial correlation increases the effective variance of the OLS estimator relative to i.i.d. errors, and HC3 does not correct for this.
- Confirmed the HDD_lag1 coefficient is identical under all three SE types (Standard, HC3, HAC) — the OLS estimator is unchanged by the variance correction method.
- The HAC p-value exceeds the HC3 p-value (0.689), confirming the null holds even more clearly once serial correlation is accounted for in standard errors.

**Critique:**
The AI correctly selected `cov_type='HAC'` and recommended bandwidth 12. One distinction the AI did not initially explain: HAC SE is appropriate when errors have both heteroskedasticity AND autocorrelation; HC3 alone is sufficient if only heteroskedasticity is present. DW = 1.27 confirms both conditions hold here, so HAC is warranted rather than redundant. We added an explicit note in the code explaining this distinction so the HAC choice does not appear mechanical. The AI also did not mention that HAC inference can be conservative for very small samples (n < 50); this is not a concern at n = 310.

---

## M3 Summary of AI Use

| # | Task | Tool | Specification decisions verified by team |
|---|------|------|------------------------------------------|
| 7 | capstone_models.py | Claude Code | Dynamic OLS vs PanelOLS; lag selection; HC3 justification; WTI exclusion from Model A; caught `sm.add_constant` bug |
| 8 | Diagnostic interpretation | Claude Code | ADF borderline threshold; HC3 vs HC1/HC2 (Long & Ervin 2000); economic interpretation of tail events |
| 9 | Robustness check design | Claude Code | Crisis years selection; subsample break date; added geographic HDD check; rejected placebo test |
| 10 | Newey-West HAC SE (Bonus) | Claude Code | Bandwidth selection (12 vs data-driven 6); verified HAC vs HC3 direction; confirmed HAC warranted given DW < 2 |

**Total AI-assisted code for M3:** ~240 lines of the ~470-line `capstone_models.py`.
**Lines reviewed or modified by team:** All lines; ~20 lines modified (const-column bug fix in Model B; crisis exclusion years; removal of placebo test; geographic HDD robustness check added in full).

---

# Full Project Summary of AI Use

| Milestone | Uses | Primary tasks | Net AI contribution | Key human corrections |
|-----------|------|---------------|--------------------|-----------------------|
| M1 | 1–3 | FRED fetch, NOAA pagination, merge strategy | ~60 lines of pipeline code | Added `units='standard'`, retry handling, `assert` statement |
| M2 | 4–6 | config_paths, EDA notebook, summary doc | ~500 lines notebook/docs | Fixed axis units, changed rolling window to 24 months, added geographic mismatch flag |
| M3 | 7–10 | capstone_models.py, diagnostics, robustness, HAC SE | ~240 lines model code | Fixed `sm.add_constant` bug, added 5th robustness check, rejected placebo test, verified HAC bandwidth |

**Across all milestones:**
- All AI outputs were tested end-to-end before submission. The `sm.add_constant` bug (Use 7) demonstrates why this is non-negotiable — the script produced no visible error but would have generated wrong predictions.
- The most substantive independent contribution was the geographic mismatch identification (Use 6 / M2), which drove the switch from Boston Logan single-station HDD to EIA population-weighted NEC_HDD in M3, and motivated the fifth robustness check (Use 9) confirming the null result holds across all HDD definitions.
- Economic interpretations were validated against course materials (Gujarati, *Basic Econometrics*) and external references where relevant (Hamilton 1994, Long & Ervin 2000).
- No AI-generated economic claim was included without verification against either the computed data or a cited source.
