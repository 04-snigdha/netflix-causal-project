import pandas as pd
from dowhy import CausalModel
import os

# 1. Load Data
df = pd.read_csv("netflix_data.csv")

# 2. Naive Estimation (Correlation)
naive_lift = df[df['marketing_spend'] == 1]['viewership'].mean() - \
             df[df['marketing_spend'] == 0]['viewership'].mean()

# 3. DoWhy Causal Modeling
# We define the relationship: Holidays and Genre affect both Spend and Views
model = CausalModel(
    data=df,
    treatment='marketing_spend',
    outcome='viewership',
    common_causes=['is_holiday', 'genre_pop']
)

# Identify the causal effect
identified_estimand = model.identify_effect(proceed_when_unidentifiable=True)

# Estimate the causal effect using Linear Regression (controlling for confounders)
estimate = model.estimate_effect(
    identified_estimand,
    method_name="backdoor.linear_regression"
)

print("-" * 30)
print(f"NAIVE LIFT (Correlation): {naive_lift:.2f} Million Hours")
print(f"CAUSAL ATE (True Impact): {estimate.value:.2f} Million Hours")
print("-" * 30)

if __name__ == "__main__":
    print("Causal model processing complete.")
