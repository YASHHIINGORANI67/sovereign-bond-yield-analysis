# Sovereign Bond Yield Analysis

### Econometric Modelling | Fixed Income | Python | Statistical Analysis

## Project Overview

This project investigates the macroeconomic and credit-related determinants of 10-year sovereign government bond yields across 50 countries using cross-sectional econometric analysis.

The analysis examines how sovereign credit ratings, inflation, and government debt influence borrowing costs, applying Ordinary Least Squares (OLS) regression and statistical diagnostic tests.

## Objectives

- Identify the main determinants of sovereign bond yields.
- Examine the relationship between credit ratings, inflation, government debt, and yields.
- Estimate and evaluate cross-sectional regression models.
- Test model assumptions and investigate potential specification problems.
- Develop an improved regression specification and interpret the results.

## Dataset

The dataset contains observations for 50 countries, including:

- 10-year sovereign bond yields
- Government debt-to-GDP ratios
- Inflation rates
- Numerical sovereign credit ratings

Data source references are provided in `SOURCES.txt`.

## Methodology

**1. Exploratory Data Analysis**

Examined yield distributions, cross-country differences, and relationships between macroeconomic variables.

**2. OLS Regression**

Estimated an initial multiple linear regression model to evaluate the association between sovereign yields and the explanatory variables.

**3. Regression Diagnostics**

Applied statistical tests and visual diagnostics, including:

- Ramsey RESET test for model specification
- Breusch–Pagan test for heteroskedasticity
- Jarque–Bera test for residual normality

---

## Research question and evidence
How are sovereign 10-year yields associated with ratings, inflation and public debt in the 50-country cross-sectional sample?

**Descriptive sample:** 50 countries; mean yield 7.78%; median 4.30%; minimum 0.90%; maximum 55.0%, as calculated from the repository dataset for the portfolio. These are historical dataset values, not live bond quotations.

**Reproduction:** inspect the dataset and `SOURCES.txt`, identify the original Python analysis script, install its documented dependencies, then run it locally. Verify units and the direction of the numerical credit-rating scale before interpreting coefficients.

**Validation checklist:** report coefficient estimates, standard errors, confidence intervals and p-values from a reproducible run; review Ramsey RESET, Breusch–Pagan and Jarque–Bera diagnostics; assess influential observations and robust standard errors. No independently verified regression coefficients are asserted here.

**Limitations:** a small cross-sectional sample supports association analysis, not causal identification.
