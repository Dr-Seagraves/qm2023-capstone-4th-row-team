[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/gp9US0IQ)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=22635011&assignment_repo_type=AssignmentRepo)
# QM 2023 Capstone Project

Semester-long capstone for Statistics II: Data Analytics.

## Project Structure

- **code/** — Python scripts and notebooks. Use `config_paths.py` for paths.
- **data/raw/** — Original data (read-only)
- **data/processed/** — Intermediate cleaning outputs
- **data/final/** — M1 output: analysis-ready panel
- **results/figures/** — Visualizations
- **results/tables/** — Regression tables, summary stats
- **results/reports/** — Milestone memos
- **tests/** — Autograding test suite


Run `python code/config_paths.py` to verify paths.

# Project Planning Update

## 1. Preliminary Research Question

What is the impact of interest rates on the U.S. housing market?

Housing is one of the most interest-rate-sensitive sectors of the economy. When the Federal Reserve raises interest rates, borrowing becomes more expensive, which can reduce mortgage demand, slow home construction, and put downward pressure on home prices. Conversely, lower interest rates typically stimulate housing activity.

This project aims to examine whether changes in interest rates—particularly mortgage rates and the federal funds rate—have a statistically significant effect on housing starts, building permits, and home prices in the United States.

## 2. Datasets We Plan to Use

All data will be obtained from the Federal Reserve Economic Data (FRED) database maintained by the Federal Reserve Bank of St. Louis.

We plan to use the following monthly U.S. time series:

**Interest Rate Variables**
- 30-Year Fixed Mortgage Rate (MORTGAGE30US)
- Effective Federal Funds Rate (FEDFUNDS)
- 10-Year Treasury Rate (DGS10)

**Housing Market Variables**
- Housing Starts (HOUST)
- Building Permits (PERMIT)
- Case-Shiller U.S. National Home Price Index (CSUSHPINSA)

We may also include control variables such as:
- Unemployment Rate (UNRATE)
- Consumer Price Index (CPIAUCSL)

## 3. Empirical Direction

We will use regression analysis and graphical analysis to evaluate the relationship between interest rates and housing market outcomes.

Our approach will include:
- Plotting time trends in interest rates and housing variables
- Comparing housing activity during periods of rising versus falling rates
- Running regressions to test whether interest rates significantly affect housing starts and home prices
- Interpreting the statistical and economic significance of our results

The project will focus on economic interpretation and statistical inference rather than machine learning methods.
