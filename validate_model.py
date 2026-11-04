"""Reproducible diagnostics for the repository's 50-country sovereign yield CSV.

This is a supplementary analysis, not a replacement for the original
academic script or an out-of-sample forecast evaluation.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy.stats import jarque_bera
from statsmodels.stats.diagnostic import het_breuschpagan, linear_reset

DATA_PATH = Path(__file__).resolve().parent / "bond_yield_data.csv"


def main():
    df = pd.read_csv(DATA_PATH)
    required = {"Country", "Yield", "Debt", "Inflation", "Rating"}
    if not required.issubset(df.columns):
        raise ValueError(f"Missing columns: {sorted(required - set(df.columns))}")
    if df[list(required - {"Country"})].isna().any().any():
        raise ValueError("Missing numeric inputs")
    if not np.isfinite(df[["Yield", "Debt", "Inflation", "Rating"]].to_numpy(dtype=float)).all():
        raise ValueError("Non-finite numeric inputs")
    if (df[["Yield", "Debt", "Inflation"]] <= 0).any().any():
        raise ValueError("Log transformations require positive inputs")

    base = smf.ols("Yield ~ Debt + Inflation + Rating", data=df).fit()
    robust = base.get_robustcov_results(cov_type="HC3")
    reset = linear_reset(base, power=2, test_type="fitted", use_f=True)
    bp = het_breuschpagan(base.resid, base.model.exog)
    jb = jarque_bera(base.resid)
    cooks = base.get_influence().cooks_distance[0]
    influential = np.argsort(cooks)[-5:][::-1]

    print("Sovereign yield analysis — independent CSV-based baseline")
    print(f"Rows: {len(df)} | Mean yield: {df['Yield'].mean():.3f}%")
    print(f"OLS R-squared: {base.rsquared:.4f}")
    print("\nOLS coefficients and conventional p-values:")
    for name, coef, p in zip(base.params.index, base.params, base.pvalues):
        print(f"  {name}: coef={coef:.6g}; p={p:.4g}")
    print("\nHC3 heteroskedasticity-robust p-values:")
    for name, p in zip(base.params.index, robust.pvalues):
        print(f"  {name}: p={p:.4g}")
    print(f"\nRamsey RESET p-value: {float(reset.pvalue):.4g}")
    print(f"Breusch-Pagan p-value: {float(bp[1]):.4g}")
    print(f"Jarque-Bera p-value: {float(jb.pvalue):.4g}")
    print("\nTop 5 observations by Cook's distance:")
    for idx in influential:
        print(f"  {df.iloc[idx]['Country']}: {cooks[idx]:.4g}")
    print("\nInterpretation: descriptive cross-sectional association only.")
    print("P-values and diagnostics do not prove causality or external validity.")


if __name__ == "__main__":
    main()
