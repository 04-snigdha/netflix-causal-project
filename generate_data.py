import numpy as np
import pandas as pd

def main():
    np.random.seed(42)
    n_samples = 2000

    # 1. Genre_Pop: Random float (0-100)
    genre_pop = np.random.uniform(0, 100, n_samples)

    # 2. Is_Holiday: Binary (20% chance)
    is_holiday = np.random.binomial(1, 0.2, n_samples)

    # 3. Marketing_Spend: Binary. Heavily dependent on Is_Holiday and Genre_Pop
    # We use a logistic/sigmoid function to turn the linear combination into a probability
    logit_prob = -3.0 + 0.05 * genre_pop + 3.0 * is_holiday
    prob_marketing = 1 / (1 + np.exp(-logit_prob))
    marketing_spend = np.random.binomial(1, prob_marketing)

    # 4. Viewership: Outcome. 
    # True Effect of Marketing should be +5M hours, Holiday Effect should be +12M hours.
    # We also add an effect from Genre_Pop and some random noise.
    viewership = (
        15.0 +                            # Baseline viewership
        5.0 * marketing_spend +           # True effect of Marketing
        12.0 * is_holiday +               # Effect of Holiday
        0.2 * genre_pop +                 # Effect of Genre Popularity
        np.random.normal(0, 3.0, n_samples) # Random noise
    )

    # Compile into a DataFrame
    df = pd.DataFrame({
        'Genre_Pop': genre_pop,
        'Is_Holiday': is_holiday,
        'Marketing_Spend': marketing_spend,
        'Viewership': viewership
    })

    # Save to CSV
    df.to_csv('netflix_data.csv', index=False)
    print("Successfully generated netflix_data.csv with 2,000 rows.")

if __name__ == "__main__":
    main()
