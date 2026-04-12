# AI Audit Appendix — Milestones 2 & 3

**QM 2023 Capstone | 4th Row Team | March 2026**

---

## Purpose

This appendix documents all uses of AI tools (Claude, GitHub Copilot, ChatGPT, etc.) during
the development of Milestone 2. For each use, we describe the prompt given, the output received,
how it was verified, and our critical assessment of the output quality.

---

## AI Tool Uses

### Use 1 — `config_paths.py` Module Design

**Tool:** Claude (claude-sonnet-4-6 via Claude Code CLI)

**Prompt given:**
> "The project is missing a config_paths.py that was flagged in M1 feedback. Create one that
> defines project root, all data directories, results/figures dir, and key file paths. It
> should create directories on import."

**Output received:**
A Python module using `pathlib.Path(__file__).resolve().parent` to anchor paths to the project
root regardless of calling directory, with `mkdir(parents=True, exist_ok=True)` guards.

**Verification:**
- Read the generated file manually and confirmed all paths match the actual project directory structure.
- Tested that `from config_paths import FIGURES_DIR` resolves correctly from both the project root
  and from within the `code/` subdirectory.
- Confirmed that FIGURES_DIR points to `results/figures/` as required by the assignment rubric.

**Critique:**
The design is clean and robust. One potential issue: if the project is moved or zipped and
extracted to a different path, `Path(__file__)` still works correctly (unlike hardcoded paths).
We added the `for _dir in [...]: _dir.mkdir(...)` loop ourselves after reviewing the output,
to ensure idempotent directory creation. The AI correctly used `exist_ok=True` to prevent errors
on repeated imports.

---

### Use 2 — EDA Notebook Structure Planning

**Tool:** Claude (claude-sonnet-4-6 via Claude Code CLI)

**Prompt given:**
> "Build a complete capstone_eda.ipynb for a single-entity monthly time series dataset with
> outcome = Real Heating Oil Price and driver = Heating Degree Days (Boston Logan). Dataset
> has no natural grouping variable. Implement all 8 required M2 plots per the assignment rubric:
> correlation heatmap, time series, dual-axis, lag analysis, rolling correlation (Alternative B),
> time period subsample (Alternative A), scatter plots, and decomposition. All plots must be
> saved to FIGURES_DIR at 300 DPI. Include economic captions for each plot."

**Output received:**
A complete Jupyter notebook (nbformat 4) with 8 visualization cells, economic narrative cells,
summary statistics, and feature engineering (real price in 2020 dollars, lagged HDD variables,
period classification).

**Verification:**
- Reviewed all column name references against `data/final/final.csv` header row to confirm
  they match exactly: `YearMonth`, `Heating_Oil_Price`, `CPI`, `Real_Heating_Oil_Price`,
  `Heating_Degree_Days`.
- Verified that `pd.to_datetime(df['YearMonth'], format='%Y-%m')` correctly parses the
  "YYYY-MM" string format used in the CSV.
- Confirmed that `seasonal_decompose(ts, model='additive', period=12)` is appropriate for
  a monthly series — period=12 matches the annual heating cycle.
- Checked that all 8 required plots are present and saved with descriptive filenames.
- Reviewed the rescaling formula `Real_Price_2020 = Heating_Oil_Price * (CPI_2020_REF / CPI)`
  and confirmed it correctly expresses prices in 2020 constant dollars.
- Confirmed `FIGURES_DIR` is used (not a hardcoded path) for all `plt.savefig()` calls.

**Critique:**
The AI correctly identified that with no grouping variable, alternatives A and B should replace
Plots 5–6, which directly matches the assignment guidance. The economic captions are plausible
but reference expected correlation signs and economic mechanisms that should be updated with
actual computed values after running the notebook. The choice to use rolling 24-month correlation
as Alternative B is particularly well-suited to the research question (does globalization weaken
the winter–price link?), as it directly visualizes structural change over time. One area of
improvement: the AI initially used `Real_Heating_Oil_Price` directly for visualization, but
we requested it use a rescaled 2020-dollar version for more interpretable axis labels — this
was incorporated in the final output.

---

### Use 3 — Interactive Dashboard (`create_dashboard.py`)

**Tool:** Claude (claude-sonnet-4-6 via Claude Code CLI)

**Prompt given:**
> "Create a standalone Python script that generates a self-contained HTML interactive dashboard
> using Plotly (no server required). Include the time series, dual-axis, lag bar chart, rolling
> correlation, scatter by regime, and decomposition charts. The HTML should use a clean two-column
> grid layout and include captions."

**Output received:**
A Python script using `plotly.graph_objects` and `plotly.express` to generate six interactive
figures, assembled into a custom HTML file with CSS grid layout, header, and figure captions.

**Verification:**
- Reviewed all Plotly trace types used (`go.Scatter`, `go.Bar`, `make_subplots`).
- Confirmed `pio.to_html(fig, full_html=False, include_plotlyjs=False)` correctly generates
  embeddable chart HTML without duplicate Plotly.js includes.
- The CDN script tag (`plotly-latest.min.js`) is included once at the top; confirmed this
  pattern is correct for self-contained HTML files.
- Verified the output file path uses `RESULTS_DIR / 'dashboard.html'` from `config_paths`.

**Critique:**
The dashboard is a strong complement to the static notebook figures. One limitation noted:
the CDN-based Plotly.js requires an internet connection to render. For fully offline use,
`include_plotlyjs=True` in one of the `pio.to_html()` calls would embed the 3MB Plotly bundle.
We left the CDN version as it keeps the file size small and the class has internet access.
The AI correctly structured the `make_subplots` call for the decomposition chart with shared
x-axes, which would have been easy to get wrong.

---

### Use 4 — EDA Summary Document (`M2_EDA_summary.md`)

**Tool:** Claude (claude-sonnet-4-6 via Claude Code CLI)

**Prompt given:**
> "Write M2_EDA_summary.md with key findings, M3 hypotheses, and data quality flags. Base it
> on the analysis in capstone_eda.ipynb — the dataset is Real Heating Oil Price vs. Boston Logan
> HDD, 2000-2024, single entity time series, no groups. Three hypotheses required: main driver
> (HDD effect), structural break (shale era), and seasonal dummy."

**Output received:**
A comprehensive markdown document with 5 key findings (each with economic mechanism), 3 M3
hypotheses (each with model specification, expected sign, and mechanism), and a data quality
table with 7 flags and mitigations.

**Verification:**
- All economic mechanisms cited are consistent with standard energy economics literature
  (commodity pricing, U.S. shale revolution chronology, HDD as demand proxy).
- The model specifications are syntactically and semantically correct for time-series OLS.
- The note about geographic mismatch (Boston Logan HDD vs. national average price) is an
  important and valid limitation that we added based on our own review of the data sources.
- The structural break dates (2008 GFC, 2014 shale glut) align with the rolling correlation
  visualization (Figure 5) and are economically justified.

**Critique:**
The AI produced thorough and economically literate analysis. The main limitation is that some
coefficient magnitudes in Hypothesis 1 ("likely in the range of $0.001–0.003/gal per HDD")
are informed estimates rather than computed values — these will be updated with actual regression
output in M3. The data quality table is more comprehensive than strictly required, which we
considered a feature rather than a bug given the assignment emphasis on M3 preparation.

---

## Summary of AI Use

| # | Task | Tool | Time saved | Human review effort |
|---|------|------|-----------|---------------------|
| 1 | config_paths.py | Claude Code | ~20 min | Verified paths, tested imports |
| 2 | capstone_eda.ipynb | Claude Code | ~4 hours | Verified all code, column names, formulas |
| 3 | create_dashboard.py | Claude Code | ~2 hours | Verified Plotly API calls, HTML structure |
| 4 | M2_EDA_summary.md | Claude Code | ~1 hour | Verified economic claims, added geographic-mismatch flag |

**Total AI-assisted code:** ~700 lines across all files.
**Total lines written/verified by team:** All lines reviewed; ~80 lines added or modified after
AI output (geographic mismatch flag, rescaling decision, rolling window choice of 24 months).

All AI outputs were treated as first drafts subject to human verification and correction.
Economic interpretations were validated against course materials and external sources.

---

# AI Audit Appendix — Milestone 3

**QM 2023 Capstone | 4th Row Team | April 2026**

---

## Purpose

This section documents all AI tool uses during Milestone 3 (Econometric Models). Per assignment requirements, emphasis is on econometric specification decisions, diagnostic test interpretations, and robustness check design.

---

## AI Tool Uses — M3

### Use 5 — Econometric Specification Design

**Tool:** Claude (claude-sonnet-4-6 via Claude Code CLI)

**Prompt given:**
> "Read the M3 milestone rubric and the existing codebase. Our dataset is a single monthly time
> series (no entity dimension) — 311 obs, Jan 2000–Dec 2025. Outcome: Real Heating Oil Price.
> Driver: HDD (Boston Logan). Key M2 finding: HDD has near-zero raw correlation with price;
> AR(1) ≈ 0.95. Design and implement capstone_models.py covering Model A (Dynamic OLS with
> AR(1) + HDD + controls), required diagnostics (Breusch-Pagan, VIF, residual plots), at least
> 3 robustness checks, and Model B (ML Comparison: OLS vs Random Forest)."

**Output received:**
A complete `capstone_models.py` script with:
- Model A: Dynamic OLS in three specifications (standard SE, HC3 robust SE, HDD×Post2014 interaction)
- ADF stationarity test with interpretation
- Breusch-Pagan test, VIF, residuals-vs-fitted and Q-Q plots
- Four robustness checks (SE comparison, lag structures 0–3, crisis-period exclusion, pre/post-2014 subsample)
- Publication-ready regression table saved to CSV
- Model B: chronological 80/20 train/test split with OLS vs Random Forest vs naive baseline

**Verification of econometric specification decisions:**

1. **Why Dynamic OLS instead of PanelOLS:** Our data has a single entity (one price series, one weather station). PanelOLS requires multiple entities to estimate entity fixed effects; applying it to one entity is meaningless. Dynamic OLS with a lagged dependent variable is the standard approach for single-entity time series with persistent autocorrelation. We verified this against the textbook treatment (Hamilton 1994, Ch. 17) and the rubric's own guidance ("Dynamic OLS" as an alternative to Fixed Effects).

2. **Why HDD at lag 1:** M2 (Plot 4, lagged correlation analysis) showed the bivariate correlation is near zero at all lags 0–12. Lag 1 is the economically motivated choice (a cold month affects next month's prices through inventory drawdown and forward purchasing). The lag-structure robustness check (Robustness 2) confirms lag selection is not driving results — all lags 0–3 yield p > 0.60.

3. **Why HC3 robust SE:** Breusch-Pagan (LM = 26.40, p < 0.0001) confirms heteroskedasticity. HC3 is preferred over HC1/HC2 in samples of this size because it provides better finite-sample coverage by downweighting leverage points — appropriate given our crisis-period outliers (2008, 2022).

4. **Why include Post2014 dummy instead of time trend:** A linear time trend assumes the price trend is smooth and monotone; our series has a non-monotone super-cycle (rising 2000–2008, falling 2009–2016, rising again). A regime dummy for the shale era (2014 onward) captures the structural level shift identified in M2 without imposing a parametric trend shape.

5. **Why ML Comparison for Model B:** The research question is fundamentally about whether local weather contributes to price variation beyond global commodity cycles. Random Forest feature importance provides a model-free, nonlinear answer: even with full flexibility, HDD gets 0.5% of importance versus 85% for lagged price and 14% for WTI. This directly answers the research question and does not require assuming linearity.

**Critique:**
The AI correctly flagged that `sm.add_constant` silently skips adding a constant when it detects a near-constant column (Post2014=1 for all test observations, since the test set is 2020–2025). This caused an initial `ValueError: shapes not aligned` that was caught during testing and fixed by manually inserting a `const` column. Without running the script, this bug would not have been caught. All generated code was tested end-to-end before submission.

The AI also correctly identified that a naive baseline (last observed value) R² of -2.73 is not a bug — it reflects that the test period (2020–2025) includes the COVID price collapse and recovery, making a frozen-last-value forecast wildly wrong. This is the correct benchmark to demonstrate that any model needs to track the series, not just hold the last value.

---

### Use 6 — Diagnostic Interpretation

**Tool:** Claude (claude-sonnet-4-6 via Claude Code CLI)

**Prompt given:**
> "Interpret the M3 diagnostic results: ADF p=0.047 (borderline), BP LM=26.40 p<0.0001,
> VIF all<1.32, residual plots showing leptokurtic tails and heteroskedastic scatter at high
> fitted values. Write the diagnostics section of M3_interpretation.md."

**Output received:**
Interpretation of each diagnostic with: statistical result, implication for inference, fix applied, and confirmation that the fix does not alter the substantive conclusion.

**Verification:**
- ADF borderline result (p = 0.047): We verified against the critical values printed by statsmodels (5% = -2.871; our statistic = -2.884, just past the threshold). The borderline classification is accurate. The Dynamic OLS AR(1) specification is robust whether the series is I(0) or near-I(1).
- Kurtosis ≈ 8.2: Confirmed this reflects the 2008 and 2022 tail events. OLS is consistent under non-normal errors; the Gauss-Markov theorem does not require normality. The caveat about finite-sample confidence interval coverage is appropriate.
- HC3 vs HC1/HC2 distinction: We verified the AI's preference for HC3 against Long & Ervin (2000) "Using Heteroscedasticity Consistent Standard Errors in the Linear Regression Model" — HC3 is recommended for n < 250, but is conservative and appropriate for n = 310 with outlier leverage points.

**Critique:**
The diagnostic interpretation is economically accurate and appropriately hedged. The AI correctly noted that leptokurtosis does not bias OLS estimates (it affects SEs and CI coverage), which is a common misconception. The note that "OLS is unbiased under non-normality" is correct (Gauss-Markov holds under E[ε|X]=0 and homoskedasticity; normality is only required for exact finite-sample inference).

---

### Use 7 — Robustness Check Design

**Tool:** Claude (claude-sonnet-4-6 via Claude Code CLI)

**Prompt given:**
> "Design at least 3 robustness checks appropriate for our dynamic OLS model on a single monthly
> time series. The rubric options are: robust SE, alternative lags, exclude outlier periods,
> group subsamples. Our main concern is: is the null HDD result real or an artifact of (a) our
> choice of lag 1, (b) crisis-period heteroskedasticity, or (c) the Post-2014 structural break?"

**Output received:**
Four robustness checks:
1. Standard SE vs HC3 (already implemented in Model 1 vs 2)
2. HDD at lags 0, 1, 2, 3 — all coefficients and p-values
3. Re-estimate excluding 2008-09 and 2020 crisis years
4. Pre-2014 vs Post-2014 subsample split

**Verification:**
- Lag structure: We confirmed that all four lags are economically defensible. Lag 0 = contemporaneous demand effect; lag 1 = next-month delivery pricing; lags 2-3 = longer-horizon forward contract pricing. All are plausible channels.
- Crisis exclusion: We excluded 2008-09 (GFC) and 2020 (COVID) specifically, not 2022 (Ukraine war), because the research question focuses on the globalization/shale structural change rather than geopolitical shocks. This is a judgment call we made independently of the AI output.
- Subsample split at 2014: The AI correctly used the shale revolution threshold from M2. We independently confirmed that U.S. crude production surpassed 9 mb/d in late 2014, the year Saudi Arabia declined to cut OPEC quotas — both supply-side events that justify a 2014 break.

**Critique:**
The AI suggested including a "placebo test" (run DiD as if shock occurred in earlier period). We did not implement this because we are not running a Difference-in-Differences model — our Post2014 dummy is a level-shift control, not a causal treatment effect. We noted this in the interpretation memo (Section: Caveats — Parallel Trends Not Applicable). Adapting AI suggestions to our specific context required human judgment.

---

## M3 Summary of AI Use

| # | Task | Tool | Specification decisions verified by team |
|---|------|------|------------------------------------------|
| 5 | capstone_models.py | Claude Code | Dynamic OLS vs PanelOLS; lag choice; HC3 justification; Post2014 vs trend |
| 6 | Diagnostic interpretation | Claude Code | ADF borderline threshold; HC3 vs HC1/HC2; OLS unbiasedness under non-normality |
| 7 | Robustness check design | Claude Code | Crisis years to exclude; subsample split date; placebo test inapplicability |

**Total AI-assisted code for M3:** ~280 lines in `capstone_models.py`.
**Total lines reviewed/corrected by team:** All lines; ~15 lines modified after initial generation
(const-column bug fix in Model B; crisis exclusion years; removal of placebo test).

All specification decisions, diagnostic interpretations, and robustness conclusions were verified by the team against econometrics course materials, textbook references, and the M2 EDA findings before inclusion in this submission.
