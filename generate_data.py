import pandas as pd
import numpy as np
import os
from datetime import datetime

def generate_netflix_data(n=2000):
    np.random.seed(42)
    
    # Confounders
    genre_pop = np.random.uniform(0, 100, n)
    is_holiday = np.random.binomial(1, 0.2, n)
    
    # Treatment (Marketing) - Biased by holiday and genre
    # We want marketing to be more likely during holidays/popular genres
    marketing_score = (0.4 * genre_pop) + (5 * is_holiday) + np.random.normal(0, 5, n)
    marketing_spend = np.where(marketing_score > 25, 1, 0)
    
    # Outcome (Viewership) - The "True" marketing effect is 5M
    # The Holiday effect is 12M (the confounder)
    noise = np.random.normal(0, 2, n)
    viewership = (5 * marketing_spend) + (12 * is_holiday) + (0.1 * genre_pop) + noise
    
    df = pd.DataFrame({
        'genre_pop': genre_pop,
        'is_holiday': is_holiday,
        'marketing_spend': marketing_spend,
        'viewership': viewership
    })
    
    return df

if __name__ == "__main__":
    df = generate_netflix_data()
    df.to_csv("netflix_data.csv", index=False)
    print(f"Success: 'netflix_data.csv' created with {len(df)} rows.")
