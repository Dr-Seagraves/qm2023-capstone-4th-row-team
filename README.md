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

1. Research Question
The Economic Shield: Have efficiency gains made home budgets "immune" to heating oil volatility?

Does a freezing winter still "break the bank" for the average family? This project examines if 30 years of home improvements have created a shield for the consumer. We are testing if the link between extreme weather and financial stress is weakening because our homes are finally good enough to "ignore" the outside temperature.

2. Datasets
We will use three primary government sources to build this "Resilience Index":

Climate Stress (NOAA): Heating Degree Days (HDD). This measures exactly how hard the weather "pushed" against our homes.

Energy Response (EIA): Residential Distillate Fuel Oil Sales. This tracks the actual gallons consumed to fight the cold.

Economic Impact (FRED): Real Heating Oil Prices (Nominal prices divided by CPI). This helps us see if people are using less oil because their homes are better, or just because they can't afford it.

3. Empirical Direction
We will evaluate the "Shield" by looking at the data in three ways:

The Consumption Slope: We will compare the 1990s to the 2020s. We expect to see that for every 10% increase in cold weather, the corresponding spike in oil buying is much smaller today than it was 30 years ago.

Price vs. Efficiency: We will analyze years with high oil prices. If oil use dropped and stayed low even after prices fell, it proves that homeowners made permanent efficiency upgrades (like new windows) rather than just "suffering through the cold."

Extreme Weather Stress Test: We will isolate the "Polar Vortex" years. If the total energy cost for a house in a record-breaking cold year today is lower (after inflation) than a "normal" year in 1990, the "Thermal Fortress" theory is proven.
