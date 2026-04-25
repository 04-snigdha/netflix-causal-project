import pandas as pd
import numpy as np
from dowhy import CausalModel
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

def main():
    print("Loading data...")
    df = pd.read_csv('netflix_data.csv')

    print("Defining causal model...")
    # Define the causal graph explicitly
    causal_graph = """
    digraph {
        is_holiday_season -> marketing_spend;
        is_holiday_season -> viewership_hours;
        marketing_spend -> viewership_hours;
        genre_popularity -> viewership_hours;
        genre_popularity -> marketing_spend;
    }
    """

    model = CausalModel(
        data=df,
        treatment='marketing_spend',
        outcome='viewership_hours',
        graph=causal_graph
    )

    print("Identifying causal effect...")
    identified_estimand = model.identify_effect(proceed_when_unidentifiable=True)

    print("Estimating causal effect...")
    estimate = model.estimate_effect(
        identified_estimand,
        method_name="backdoor.linear_regression",
        test_significance=True
    )

    print(f"\n--- Estimated ATE ---")
    print(f"Estimated Average Treatment Effect: {estimate.value:.4f}")

    print("\n--- Running Robustness Tests ---")
    
    print("\n1. Placebo Treatment Refuter (Should drop to ~0)")
    refutation_placebo = model.refute_estimate(
        identified_estimand, 
        estimate,
        method_name="placebo_treatment_refuter",
        placebo_type="permute"
    )
    print(refutation_placebo)

    print("\n2. Random Common Cause Refuter (Should remain stable)")
    refutation_random = model.refute_estimate(
        identified_estimand,
        estimate,
        method_name="random_common_cause"
    )
    print(refutation_random)

if __name__ == "__main__":
    main()
