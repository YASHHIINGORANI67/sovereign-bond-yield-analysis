# Sovereign Bond Yield Analysis

**Econometrics | Fixed income | Sovereign credit risk | Python | Cross-sectional OLS**

## Overview

This project investigates associations between **10-year sovereign government bond yields** and macroeconomic or credit-related characteristics across a **50-country cross-sectional sample**.

The study considers sovereign credit ratings, inflation and government debt using exploratory analysis, Ordinary Least Squares (OLS) regression and statistical diagnostics.

> **Evidence note:** The descriptive sample statistics below were previously calculated from the repository dataset for the portfolio. They are historical observations, **not live bond quotations**. Regression coefficients and p-values are not independently verified in this README.

## Research question

**How are sovereign 10-year yields associated with credit ratings, inflation and public debt in the 50-country sample?**

## Data and variables

| Variable | Role |
|---|---|
| 10-year sovereign bond yield | Dependent variable |
| Numerical sovereign credit rating | Explanatory variable; coding direction must be checked |
| Inflation rate | Explanatory variable |
| Government debt-to-GDP ratio | Explanatory variable |

The dataset covers 50 countries. Original data references are listed in `SOURCES.txt`; consult that file for source provenance and coverage.

## Descriptive sample results

| Statistic | Historical sample value |
|---|---:|
| Countries | 50 |
| Mean 10-year yield | 7.78% |
| Median 10-year yield | 4.30% |
| Minimum yield | 0.90% |
| Maximum yield | 55.00% |

The gap between the mean and median and the high maximum indicate that unusually high-yield observations warrant attention in model diagnostics. These summary statistics alone do not establish the direction or statistical significance of any explanatory relationship.

## Empirical approach

1. **Exploratory data analysis:** Review distributions, country-level differences and bivariate relationships.
2. **OLS regression:** Estimate cross-sectional associations between yields, ratings, inflation and public debt.
3. **Model diagnostics:** Examine assumptions and specification using the tests reported in the project:
   - **Ramsey RESET** — functional form and specification.
   - **Breusch–Pagan** — heteroskedasticity.
   - **Jarque–Bera** — residual normality.
4. **Interpretation:** Evaluate the direction, scale and uncertainty of estimated relationships, with attention to rating coding and influential countries.

## Reproduction guidance

1. Review the repository dataset and `SOURCES.txt` to confirm variable definitions, sources and units.
2. Locate the original Python analysis script in the repository and inspect its imports and input paths.
3. Install the dependencies required by that script, then run it locally against the supplied dataset.
4. Compare descriptive statistics and regression output with the academic materials.
5. Record package versions, missing-value treatment and any data transformations for repeatability.

A pinned environment, automated tests and an independently verified coefficient table are **not established** here.

## Validation roadmap

**Recommended checks — not independently confirmed results:**
- Report OLS coefficients, standard errors, confidence intervals and p-values from a reproducible run.
- Check the direction and ordinal interpretation of the numeric credit-rating scale.
- Review RESET, Breusch–Pagan and Jarque–Bera outcomes.
- Consider heteroskedasticity-robust standard errors and influential-observation diagnostics.
- Examine the effect of high-yield countries and alternative model specifications.

## Limitations

A 50-country cross-section supports **associational**, not causal, inference. Omitted factors, cross-country heterogeneity, rating endogeneity, outliers and measurement differences may affect the estimates. Findings should not be interpreted as real-time forecasts or investment recommendations.

## Tools and related work

**Tools:** Python · OLS regression · Econometric diagnostics · Sovereign fixed-income analysis

**Portfolio:** [Financial Risk Research — Yash Hingorani](https://yashhiingorani67.github.io/) · [LinkedIn](https://www.linkedin.com/in/yashhingorani)

## Reproducible environment and data checks

The repository now includes a [dependency manifest](requirements.txt) derived from the imports in `Final_bond_analysis.py` and a [standard-library data-integrity test suite](tests/test_dataset.py).

From the repository root, using a supported Python 3 environment:

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python Final_bond_analysis.py
```

The tests check the CSV column names, 50 unique countries, finite positive numeric inputs needed for logarithms, and documented descriptive yield statistics. **They do not test coefficient accuracy, statistical significance, forecast performance or the validity of the source observations.**

**Execution caveat:** The original script embeds its own 50-country CSV text rather than reading `bond_yield_data.csv`. Its charts open interactive windows and its final `input()` prompt requires user interaction; run it locally in a graphical environment. The dependency manifest specifies compatible version ranges based on imports, not a tested lockfile. Automated execution of the full analysis has not been verified here. The script's statements that transformations “fix” diagnostics should be treated as hypotheses requiring post-transformation diagnostic tests, not established facts.
