# AI Audit Appendix — Milestone 2

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
