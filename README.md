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
