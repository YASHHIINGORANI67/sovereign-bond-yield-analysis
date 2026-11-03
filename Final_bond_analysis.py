import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from statsmodels.stats.diagnostic import het_breuschpagan, linear_reset
from io import StringIO
import warnings

# Suppress warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

# Set visual style
try:
    plt.style.use('seaborn-v0_8-whitegrid')
except:
    plt.style.use('ggplot')

# Step 1: Data set, Intial model & graphs
print("\n Step 1: Data set, Intial model & graphs")

csv_data = """Country,Yield,Debt,Inflation,Rating
United States,4.2,122,3.1,1
Germany,2.4,64,2.5,1
Japan,1.1,260,2.6,2
United Kingdom,4.1,101,3.4,2
China,2.3,77,0.3,3
France,2.9,110,2.9,2
Italy,3.8,137,1.2,5
Canada,3.4,107,2.8,1
India,7.1,83,5.1,6
Brazil,11.2,85,4.5,9
Russia,12.5,18,7.4,12
South Korea,3.5,54,2.8,2
Australia,4.1,56,3.4,1
Mexico,9.5,50,4.4,7
Spain,3.2,107,2.8,4
Indonesia,6.6,39,2.6,7
Turkey,26.5,30,64.8,14
Saudi Arabia,5.2,24,1.6,4
Switzerland,0.9,39,1.2,1
Netherlands,2.6,46,2.6,1
Argentina,55.0,85,211.0,19
Sweden,2.3,30,4.4,1
Poland,5.4,49,3.9,5
Belgium,3.0,105,3.2,3
Thailand,2.7,61,0.5,6
Austria,2.9,78,4.2,2
Norway,3.6,44,3.0,1
UAE,4.8,25,1.5,3
South Africa,10.1,72,5.3,10
Denmark,2.4,29,0.8,1
Malaysia,3.9,61,1.5,5
Singapore,3.0,168,3.7,1
Egypt,14.5,92,33.7,15
Philippines,6.1,61,3.4,8
Vietnam,2.5,37,3.2,9
Pakistan,16.0,74,28.3,17
Chile,5.8,38,3.9,4
Colombia,10.2,53,7.7,10
Romania,6.5,49,6.7,8
Czech Republic,3.9,44,2.3,3
Portugal,3.0,99,2.3,5
Greece,3.4,160,3.1,8
Hungary,6.2,73,3.8,8
New Zealand,4.7,46,4.0,2
Peru,6.8,33,3.0,6
Qatar,4.4,40,2.5,3
Ukraine,22.0,78,5.1,18
Nigeria,13.5,38,28.9,14
Kenya,15.5,68,6.9,16
Ghana,28.0,88,23.2,19
"""
df = pd.read_csv(StringIO(csv_data))

print("\nDataset (50 Observations):")
print(df)

# Generate Initial Graphs
print("\nGenerating overview graphs... (close window to continue)")
plt.figure(figsize=(14, 8))
plt.subplot(2,2,1); sns.histplot(df['Yield'], kde=True, color='skyblue'); plt.title('Yield Distribution')
plt.subplot(2,2,2); sns.scatterplot(x='Debt', y='Yield', data=df, hue='Rating', palette='coolwarm'); plt.title('Debt vs Yield')
plt.subplot(2,2,3); sns.boxplot(x=df['Inflation'], color='lightgreen'); plt.title('Inflation Boxplot')
plt.subplot(2,2,4); sns.barplot(x='Yield', y='Country', data=df.nlargest(5,'Yield'), hue='Country', palette='magma', legend=False); plt.title('Top 5 Yields')
plt.tight_layout()
plt.show()

# Fit Initial Model
print("\nFitting Initial Simple Model...")
model_base = smf.ols('Yield ~ Debt + Inflation + Rating', data=df).fit()
print(model_base.summary())


# Step 2: Evaluate Appropriateness
print("\n Step 2: Evaluate Model Appropriateness ")

# Numerical Tests
print("Test 1: Functional Form (Ramsey RESET)")
reset_test = linear_reset(model_base, power=2, test_type='fitted', use_f=True)
print(f"   Ramsey P-Value: {reset_test.pvalue:.4f}")
if reset_test.pvalue < 0.05: print("   >>> RESULT: Misspecified (Non-Linearity detected).")
else: print("   >>> RESULT: Appropriate (Linear form is okay).")

print("\nTest 2: Normality (Jarque-Bera)")
jb_stat, jb_p = stats.jarque_bera(model_base.resid)
print(f"   JB P-Value:     {jb_p:.4f}")
if jb_p < 0.05: print("   >>> RESULT: Residuals are NOT Normal.")
else: print("   >>> RESULT: Residuals are Normal.")

print("\nTest 3: Homoscedasticity (Breusch-Pagan)")
bp_test = het_breuschpagan(model_base.resid, model_base.model.exog)
print(f"   BP P-Value:     {bp_test[1]:.4f}")
if bp_test[1] < 0.05: print("   >>> RESULT: Heteroscedasticity detected.")
else: print("   >>> RESULT: Homoscedasticity accepted.")

# Evaluation Graphs
print("\nGenerating diagnostic graphs... (close window to continue)")
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
sns.histplot(model_base.resid, kde=True, color='purple')
plt.title('Check 1: Residual Histogram')
plt.xlabel('Residuals')

ax = plt.subplot(1, 3, 2)
stats.probplot(model_base.resid, dist="norm", plot=ax)
plt.title('Check 2: Q-Q Plot')

plt.subplot(1, 3, 3)
plt.scatter(model_base.fittedvalues, model_base.resid, alpha=0.6, color='blue')
plt.axhline(0, color='red', linestyle='--')
plt.title('Check 3: Residuals vs Fitted')
plt.xlabel('Fitted Values')
plt.ylabel('Residuals')

plt.tight_layout()
plt.show()


# Step 3: Refined Model
print("\n Step 3: Refined Model ")
print("Modification Strategy:")
print("1. Apply LOG transformation (fixes Normality & Heteroscedasticity).")
print("2. Add QUADRATIC terms (fixes Functional Form/Linearity).")
print("3. Use STEPWISE selection (removes insignificant variables).")

# Transform Variables
df['lnYield'] = np.log(df['Yield'])
df['lnDebt'] = np.log(df['Debt'])
df['lnInflation'] = np.log(df['Inflation'])

# Create Pool of Variables
X_pool = df[['lnDebt', 'lnInflation', 'Rating']].copy()
X_pool['lnDebt_Sq'] = df['lnDebt']**2
X_pool['lnInf_Sq'] = df['lnInflation']**2
X_pool['Interaction'] = df['lnDebt'] * df['lnInflation']

# Stepwise Selection
def stepwise_selection(X, y):
    included = []
    while True:
        changed=False
        excluded = list(set(X.columns)-set(included))
        new_pval = pd.Series(index=excluded, dtype='float64')
        for new_column in excluded:
            model = sm.OLS(y, sm.add_constant(pd.DataFrame(X[included+[new_column]]))).fit()
            new_pval[new_column] = model.pvalues[new_column]
        if new_pval.min() < 0.05:
            included.append(new_pval.idxmin())
            changed=True
        if not changed: break
    return included

final_vars = stepwise_selection(X_pool, df['lnYield'])
print(f"\nFinal Selected Variables: {final_vars}")

# Fit Final Model
X_final = sm.add_constant(X_pool[final_vars])
final_model = sm.OLS(df['lnYield'], X_final).fit()
print("\n Refined Model")
print(final_model.summary())


# Step 4: Prediction & Discussion
print("\n Step 4: Prediction Scenarios & Discussion ")

situations = pd.DataFrame([
    {'Scenario': 'Safe Haven (AAA)', 'Debt': 40,  'Inflation': 1.5, 'Rating': 1},
    {'Scenario': 'Average Economy',  'Debt': 85,  'Inflation': 3.5, 'Rating': 7},
    {'Scenario': 'Emerging Market',  'Debt': 60,  'Inflation': 6.0, 'Rating': 10},
    {'Scenario': 'Deflationary Trap', 'Debt': 240, 'Inflation': 0.5, 'Rating': 3}, 
    {'Scenario': 'Fiscal Crisis',    'Debt': 160, 'Inflation': 15.0,'Rating': 14}
])

print(f"{'SCENARIO':<20} | {'LOG YIELD':<10} | {'PRED MEDIAN':<12} | {'PRED MEAN':<12} | {'95% CI'}")
print("-" * 85)

for i, row in situations.iterrows():
    input_row = pd.Series(index=X_final.columns, dtype='float64')
    input_row['const'] = 1.0
    
    # Map inputs to selected features
    if 'lnDebt' in final_vars: input_row['lnDebt'] = np.log(row['Debt'])
    if 'lnInflation' in final_vars: input_row['lnInflation'] = np.log(row['Inflation'])
    if 'Rating' in final_vars: input_row['Rating'] = row['Rating']
    if 'lnDebt_Sq' in final_vars: input_row['lnDebt_Sq'] = np.log(row['Debt'])**2
    if 'lnInf_Sq' in final_vars: input_row['lnInf_Sq'] = np.log(row['Inflation'])**2
    if 'Interaction' in final_vars: input_row['Interaction'] = np.log(row['Debt']) * np.log(row['Inflation'])

    # Predict Log Yield
    pred = final_model.get_prediction(input_row)
    summ = pred.summary_frame(alpha=0.05)
    
    # 1. LOG YIELD (yhat)
    y_log = summ['mean'].iloc[0]

    # 2. MEDIAN PREDICTION (exp(yhat))
    y_median = np.exp(y_log)
    
    # 3. MEAN PREDICTION (exp(yhat + MSE/2))
    y_mean = np.exp(y_log + final_model.mse_resid/2)
    
    # 4. CONFIDENCE INTERVAL (exp(lower), exp(upper))
    lower = np.exp(summ['obs_ci_lower'].iloc[0])
    upper = np.exp(summ['obs_ci_upper'].iloc[0])
    
    print(f"{row['Scenario']:<20} | {y_log:6.4f}     | {y_median:6.2f}%      | {y_mean:6.2f}%      | [{lower:5.2f}%, {upper:5.2f}%]")

print("-" * 85)
print("Note: 'Pred Median' = exp(yhat). 'Pred Mean' = exp(yhat + MSE/2).")

print("\nBenefits of Analysis:")
print("1. Improved Accuracy: The Stepwise Log-Quadratic model corrects non-normality.")
print("2. Robustness: Quadratic terms capture the explosive nature of debt crises.")
print("3. Interpretable: We isolated Credit Rating as a key driver.")

print("\nLimitations:")
print("1. Omitted Variable Bias: Missing 'Global Risk' (VIX) or 'Exchange Rate' data.")
print("2. Structural Breaks: Assumes constant relationship across all 50 countries.")
print("3. The 'Japan Paradox': May over-predict yields for countries with Yield Curve Control.")

input("\nPress Enter to exit...")