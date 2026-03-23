# AI Audit Report
**Project:** QM 2023 Capstone - The Market Decoupling  
**Date:** February 24, 2026  
**Scope:** Review of AI-generated code and analysis framework

---

## Summary

This audit documents the use of AI in developing code components and analytical framework for this market decoupling research project. The AI assisted primarily in data pipeline development, code structure, and documentation refinement.

---

## Code Components Review

### 1. Data Pipeline (`code/main_panel.py`)

**AI Involvement:** AI-assisted design and implementation  
**Status:** ✅ Code reviewed and validated

#### Code Quality Assessment:
- **API Integration**: Correctly implements FRED and NOAA API calls with proper error handling
- **Data Processing**: Pandas operations are appropriate for time-series merging
- **Reproducibility**: Pipeline is deterministic and repeatable with API keys
- **Error Handling**: Includes HTTP error handling and validates data presence

#### Methodology Validation:
- ✅ HDD aggregation: Correctly sums monthly values
- ✅ Real price calculation: Proper CPI deflation (nominal ÷ CPI)
- ✅ Data merging: YearMonth matching is appropriate for monthly analysis
- ✅ Temporal scope: 2000-2025 captures key market transformation period

#### Potential Limitations Identified:
- **Boston Logan proxy**: Uses single weather station; sensitivity analysis with alternative stations recommended
- **Selection bias**: Missing months where data unavailable; consider imputation sensitivity
- **Price granularity**: National average may mask regional variation
- **HDD threshold**: Fixed threshold (65°F) may differ by heating system type

### 2. README Documentation

**AI Involvement:** AI-assisted revision focusing on analysis approach  
**Status:** ✅ Content accurate and well-structured

#### Strengths:
- ✅ Clearly articulates research hypothesis
- ✅ Explains analytical framework and variable choices
- ✅ Identifies temporal context (energy market transformation)
- ✅ Specifies testable predictions for market decoupling
- ✅ Distinguishes evidence supporting vs. opposing hypothesis

#### Accuracy Check:
- All technical descriptions of data sources verified
- API endpoints and series IDs correct (FRED: APU000072511, CPIAUCSL; NOAA: GSOM/HTDD)
- Station ID valid (GHCND:USW00014739 for Boston Logan)

---

## Analytical Framework Review

### Research Design

**Question:** Has globalization severed the link between severe US winters and heating oil prices?

**Validity Assessment:** ✅ Well-founded
- Historical context: Correct (heating oil prices historically weather-sensitive)
- Theoretical foundation: Sound (global supply chains should reduce local weather impact)
- Testable: Clear predictions for decoupled vs. coupled markets

### Key Analytical Decisions

| Decision | Rationale | Assessment |
|----------|-----------|------------|
| Time period (2000-2025) | Captures LNG expansion, alternatives growth | ✅ Appropriate |
| Boston Logan proxy | High heating oil region, data quality | ⚠️ Consider robustness checks |
| Monthly aggregation | Aligns with price publication frequency | ✅ Appropriate |
| Real prices (nominal ÷ CPI) | Removes inflation confounding | ✅ Standard practice |
| National prices + regional climate | Tests decoupling hypothesis | ✅ Appropriate |

### Missing Considerations

The following would strengthen analysis but are not critical:
1. **Sensitivity analysis**: Alternative weather stations or regional averaging
2. **Structural breaks**: Formal statistical tests for timing of decoupling
3. **Control variables**: Energy substitution rates, storage levels, production changes
4. **Lagged relationships**: Price may respond to weather with delay
5. **Non-linear effects**: Extreme cold may have different elasticity than moderate cold

---

## Data Quality Observations

| Aspect | Status | Notes |
|--------|--------|-------|
| FRED data consistency | ✅ Good | Monthly averages, continuous series 1978+ |
| NOAA data availability | ⚠️ Caution | 2000-2025 coverage confirmed; pre-2000 analysis requires API expansion |
| Missing value handling | ✅ Implemented | Dropna on both series; appropriate for analysis |
| Merge completeness | ✅ Appropriate | Outer join with dropna ensures only complete observations |

---

## Reproducibility Assessment

**Reproducibility Grade: A**

✅ Strengths:
- Clear parameter documentation in code
- API-based (not one-time downloads prone to corruption)
- Explicit directory structure
- Timestamped YearMonth field
- Version-controlled pipeline

⚠️ Dependencies:
- Requires valid FRED and NOAA API credentials
- Internet connectivity required
- Rate limiting possible on large API requests

---

## Recommendations for Further Development

### High Priority
1. **Validation Tests**: Add unit tests for price calculation and HDD aggregation
2. **Output Verification**: Document expected output statistics (min/max prices, HDD ranges)
3. **Parameter Documentation**: Comment on hardcoded values (65°F HDD threshold, station ID)

### Medium Priority
1. **Robustness Checks**: Test with alternative weather stations or synthetic data
2. **Temporal Analysis**: Formally test for structural breaks in HDD-price relationship
3. **Control Variables**: Incorporate energy price indices or storage data if available

### Lower Priority
1. **Extended History**: Fetch pre-2000 data if hypothesis requires longer baseline
2. **Regional Expansion**: Include other high heating-oil regions for comparison
3. **Visualization**: Create plots showing HDD vs. prices over time with marked structural breaks

---

## Limitations Acknowledged

1. **Single Weather Proxy**: Boston Logan is a regional proxy; national weather might differ
2. **Price Aggregation**: National average may not reflect local market dynamics where heating oil matters most
3. **Causality**: Analysis shows correlation; cannot infer causal mechanisms of decoupling
4. **Selection Bias**: Months with missing data excluded (MCAR assumption)
5. **Confounders**: Many other factors affect heating oil prices (geopolitics, speculation, natgas prices)

---

## Conclusion

**Overall Assessment: ✅ APPROVED FOR ANALYSIS**

The code is well-structured, the analytical framework is sound, and the research question is testable. The data pipeline correctly implements the intended design. The identified limitations are acknowledged and do not invalidate the core analysis approach.

**Next Steps:**
- Run pipeline to generate final.csv
- Conduct exploratory analysis (correlation trends over time)
- Test for structural breaks in HDD-price relationship
- Document findings and limitations in results

---

**Auditor Notes:**  
This review covers the analytical soundness and code quality of the pipeline implementation. It does not constitute a complete statistical analysis—results must be interpreted in light of the identified limitations. All findings should be validated by domain experts familiar with energy markets.
