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

# --- PHASE 4: REFUTATIONS ---
print("\n" + "="*30)
print("RUNNING ROBUSTNESS TESTS (REFUTATIONS)")
print("="*30)

# 1. Placebo Treatment: Replacing treatment with random noise
# Expected: New effect should be close to 0
refute_placebo = model.refute_estimate(identified_estimand, estimate,
                                     method_name="placebo_treatment_refuter")
print(f"\nPlacebo Treatment Refuter:\n{refute_placebo}")

# 2. Random Common Cause: Adding a random variable as a confounder
# Expected: New effect should be similar to the original estimate
refute_random = model.refute_estimate(identified_estimand, estimate,
                                    method_name="random_common_cause")
print(f"\nRandom Common Cause Refuter:\n{refute_random}")

# 3. Data Subset Refuter: Removing a random subset of the data
# Expected: New effect should be similar to the original estimate
refute_subset = model.refute_estimate(identified_estimand, estimate,
                                    method_name="data_subset_refuter", 
                                    subset_fraction=0.9)
print(f"\nData Subset Refuter:\n{refute_subset}")

if __name__ == "__main__":
    print("Causal model processing complete.")
